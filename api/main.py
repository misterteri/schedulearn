import config
import uvicorn
import logging

import database as db
from schedulearn import Run
from pydantic import EmailStr, BaseModel
from dotenv import load_dotenv
from logging.config import dictConfig
from sqlmodel import Session, select, col
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from auth import hash_password, encode_token, verify_password
from lib import get_docker_client

load_dotenv()
dictConfig(config.LOGGING)
logger = logging.getLogger("schedulearn")
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

@app.on_event("startup")
def on_startup():
    db.initialize()

@app.post("/signup")
async def signup(user: User):
    # check if the email contains `@gapp.nthu.edu.tw`, `@cs.nthu.edu.tw`, or `@office365.nthu.edu.tw`
    # if not, return 400
    # if yes, check if the email is in the database
    domains = ["@gapp.nthu.edu.tw", "@cs.nthu.edu.tw", "@office365.nthu.edu.tw"]
    if not any(user.email.endswith(domain) for domain in domains):
        logging.warning("Invalid email")
        raise HTTPException(status_code=400, detail="Invalid email")

    with Session(db.engine) as session:
        if session.get(db.User, user.email):
            logging.warning("Email already exists")
            raise HTTPException(
                status_code=400, 
                detail="User already exists"
            )
        session.add(
            db.User(
                email=user.email, 
                password=hash_password(user.password)
            )
        )
        session.commit()
        logging.info("User created")
        return JSONResponse(status_code=201, content={"message": "User created successfully"})

@app.post("/signin")
async def user_login(login_user: User):
    # check if the email exists in the database
    # if it does, return the user
    # if it does not, create a new user and return the user
    with Session(db.engine) as session:
        user = session.exec(select(db.User).where(db.User.email == login_user.email)).first()
        if (user is None) or (not verify_password(login_user.password, user.password)):
            logging.warning("User does not exist")
            raise HTTPException(
                status_code=400, 
                detail="User does not exist"
            )

        user.token = encode_token(user.email)
        session.commit()
        session.refresh(user)
        logging.info("A token created")
    
    return JSONResponse(status_code=200, content={"username": user.name, "email": user.email, "token": user.token})

# user sign out
@app.post("/signout")
async def user_logout(user: User):
    with Session(db.engine) as session:
        user = session.exec(select(db.User).where(db.User.email == user.email)).first()
        if user is None:
            logging.warning("User does not exist")
            raise HTTPException(
                status_code=400, 
                detail="User does not exist"
            )

        user.token = None
        session.commit()
        logging.info("A token deleted")
    
    return JSONResponse(status_code=200, content={"message": "User logged out successfully"})


@app.post("/jobs", response_model=Job, status_code=201)
async def add_job(job: Job, background_tasks: BackgroundTasks):
    "Add a job to the scheduler"
    with Session(db.engine) as session:
        job = db.Job(**job.dict())
        session.add(job)
        session.commit()
        session.refresh(job)

    background_tasks.add_task(Run, job)
    return JSONResponse(status_code=201, content={"message": "Job created successfully"})


@app.get("/jobs")
async def get_jobs():
    "Get all jobs"
    with Session(db.engine) as session:
        jobs = session.exec(
            select(db.Job)
            .order_by(col(db.Job.created_at).desc())
        ).fetchall()
        return jobs


@app.get("/jobs/{id}")
async def get_job(id: int):
    "Get status of a job"
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()
        return job

@app.websocket("/jobs/{id}/logs")
async def get_job_logs(websocket: WebSocket, id: int):
    await websocket.accept()
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()
    
    docker_client = get_docker_client(job.trained_at)
    container = docker_client.containers.get(f"{job.name}-{job.id}".lower().replace(" ", "-"))
    while True:
        for line in container.logs(stream=True, follow=True):
            await websocket.send_text(line.decode("ascii"))
        break
    
    await websocket.close()

@app.delete("/jobs/{id}", status_code=204)
async def kill_job(id: int, background_tasks: BackgroundTasks):
    """
    If a model is on progress, delete the pod immediately, as well as the
    metadata of a model in the database.
    """
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()

        # kill the container running the job
        # ....

        # delete the job from the database
        session.delete(job)
        session.commit()
    
    # kill the job in the background
    return job


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=int(config.PORT))
