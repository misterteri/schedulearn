import config
import uvicorn
import logging

import time
import asyncio
import database as db
from schedulearn import run_job, remove_job
from pydantic import EmailStr, BaseModel
from dotenv import load_dotenv
from logging.config import dictConfig
from sqlmodel import Session, select, col
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from lib import get_docker_client, log_system_status


load_dotenv()
dictConfig(config.LOGGING)
logger = logging.getLogger(__name__)
app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Job(BaseModel):
    name: str
    type: str
    container_image: str
    command: str
    required_gpus: int


class User(BaseModel):
    email: EmailStr
    password: str


async def log_system_status_task(filename: str):
    while True:
        log_system_status(filename)
        time.sleep(5)


@app.on_event("startup")
async def on_startup():
    logger.info("API starting up...")
    db.initialize()
    with Session(db.engine) as session:
        if session.exec(select(db.Schedulearn)).first() is None:
            session.add(db.Schedulearn(
                configuration="algorithm",
                value="FIFO"
            ))
            session.add(
                db.Schedulearn(
                    configuration="last_server",
                    value="gpu3"
                )
            )
            session.add(
                db.Schedulearn(
                    configuration="next_server",
                    value="gpu4"
                )
            )
            session.commit()
            logger.info("Default configuration added to database")
    logger.info("Database initialized")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("API shutting down...")
    loop = asyncio.get_event_loop()
    loop.stop()
    logger.info("All background tasks stopped")


@app.post("/jobs", response_model=Job, status_code=201)
async def add_job(job: Job, background_tasks: BackgroundTasks):
    logger.info("A training job is received")
    with Session(db.engine) as session:
        latest_job_id = session.exec(select(db.Job).order_by(col(db.Job.id).desc())).first()

        new_job = db.Job(
            id=latest_job_id.id + 1 if latest_job_id else 1,
            name=job.name,
            type=job.type,
            container_image=job.container_image,
            command=job.command,
            required_gpus=job.required_gpus,
            status="Pending"
        )

        session.add(new_job)
        session.commit()
        logger.info("A training job is added to the database")
        background_tasks.add_task(run_job, new_job.id, background_tasks)
        logger.info("A trainig job is added to the scheduler")
        return JSONResponse(status_code=201, content={"message": "Job created successfully"})

@app.put("/algorithm/{algorithm}")
async def change_algorithm(algorithm: str):
    "Change the scheduling algorithm"
    with Session(db.engine) as session:
        current_algorithm = session.exec(select(db.Schedulearn).where(db.Schedulearn.configuration == "algorithm")).first()
        if algorithm.lower() == "fifo":
            current_algorithm.value = "FIFO"
            session.commit()
            logging.info("Algorithm changed to FIFO")
            return JSONResponse(status_code=200, content={"message": "Algorithm changed to FIFO"})
        elif algorithm.lower() == "elasticfifo":
            current_algorithm.value = "ElasticFIFO"
            session.commit()
            logging.info("Algorithm changed to Elastic FIFO")
            return JSONResponse(status_code=200, content={"message": "Algorithm changed to Elastic FIFO"})
        elif algorithm.lower() == "roundrobin":
            current_algorithm.value = "RoundRobin"
            session.commit()
            logging.info("Algorithm changed to Round Robin")
            return JSONResponse(status_code=200, content={"message": "Algorithm changed to Round Robin"})
        else:
            logging.warning("Invalid algorithm")
            raise HTTPException(
                status_code=400, 
                detail="Invalid algorithm"
            )

@app.get("/jobs")
async def get_jobs():
    with Session(db.engine) as session:
        jobs = session.exec(
            select(db.Job)
            .order_by(
                col(db.Job.created_at).desc()
            )
        ).fetchall()
    logger.info("All jobs are returned")
    return jobs


@app.get("/jobs/{id}")
async def get_job(id: int):
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()
    logger.info("A job is returned")
    return job


@app.websocket("/jobs/{id}/logs")
async def get_job_logs(websocket: WebSocket, id: int):
    await websocket.accept()
    logger.info("A websocket connection is established")
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()
    
    docker_client = get_docker_client(job.trained_at)
    container = docker_client.containers.get(job.container_name)
    while True:
        for line in container.logs(stream=True, follow=True):
            await websocket.send_text(line.decode("utf-8"))
        break
    
    await websocket.close()
    logger.info("A websocket connection is closed")


@app.delete("/jobs/{id}", status_code=204,)
async def kill_job(id: int, background_tasks: BackgroundTasks):
    """
    If a model is on progress, delete the pod immediately, as well as the
    metadata of a model in the database.
    """
    background_tasks.add_task(remove_job, id)
    logger.info("A job is deleted")
    return JSONResponse(content={"message": "Job deleted successfully"})


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=int(config.PORT))