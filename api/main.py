import uuid
import time
import config
import uvicorn
import logging
import asyncio
import database as db
from dotenv import load_dotenv
from job import run_job, remove_job
from logging.config import dictConfig
from scheduler import FIFO, RoundRobin
from pydantic import EmailStr, BaseModel
from sqlmodel import Session, select, col
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from lib import get_docker_client, log_system_status
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket


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
    db.create_tables()
    db.create_servers()
    db.create_gpus()
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
async def add_job(new_job: Job, background_tasks: BackgroundTasks):
    with Session(db.engine) as session:
        scheduling_algorithm = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "algorithm")
        ).first()

        job = db.Job(
            name = new_job.name,
            type = new_job.type,
            container_name=f"{new_job.name.lower().replace(' ', '-')}-{uuid.uuid4()}",
            container_image = new_job.container_image,
            command = new_job.command,
            required_gpus = new_job.required_gpus
        )

        session.add(job)
        session.commit()
        logger.info(f"Job {job.name} added to the database")

        if scheduling_algorithm.value == "FIFO":
            destination = FIFO(job.required_gpus)
            logger.info(f"Return {len(destination.gpus)} GPUs at server {destination.server} with FIFO")
            background_tasks.add_task(run_job, job, destination, background_tasks)

        if scheduling_algorithm.value == "RoundRobin":
            destination = RoundRobin(job.required_gpus)
            logger.info(f"Return {len(destination.gpus)} GPUs at server {destination.server} with RoundRobin")
            background_tasks.add_task(run_job, job, destination, background_tasks)
            
        # if scheduling_algorithm.value == "SRJF", always sort the jobs that has started_at == None
        # A job duration is determined by job.estimated_completion_time - job.started_at
        # Sort the jobs by the duration from shortest to longest
        # Run the job with the shortest duration
        if scheduling_algorithm.value == "SRJF":
            with Session(db.engine) as session:
                jobs = session.exec(
                    select(db.Job)
                    .where(col(db.Job.started_at) == None)
                    .order_by(col(db.Job.estimated_completion_time) - col(db.Job.started_at))
                ).all()
                for job in jobs:
                    destination = FIFO(job.required_gpus)
                    logger.info(f"Return {len(destination.gpus)} GPUs at server {destination.server} with Short Remaining Job First")
                    background_tasks.add_task(run_job, job, destination, background_tasks)

    logger.info("A training job is added to the scheduler")
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