import logging
from logging.config import dictConfig
from dotenv import load_dotenv
import config
import docker
import datetime
import database as db
from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel
from sqlmodel import Session, select, col
import uvicorn

load_dotenv()
dictConfig(config.LOGGING)

logger = logging.getLogger("schedulearn")
app = FastAPI(debug=True)

client3 = docker.DockerClient(
    base_url=config.GPU3_DOCKER_HOST,
    use_ssh_client=True,
    tls=True,
)

client4 = docker.DockerClient(
    base_url=config.GPU4_DOCKER_HOST,
    use_ssh_client=True,
    tls=True,
)

client5 = docker.DockerClient(
    base_url=config.GPU5_DOCKER_HOST,
    use_ssh_client=True,
    tls=True
)

class Job(BaseModel):
    name: str
    type: str
    container_image: str
    command: str
    no_of_gpus: int

@app.on_event("startup")
def on_startup():
    db.initialize()

def run_docker(new_job):
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == new_job.id)
        ).one()
        job.started_at = datetime.datetime.now()
        session.commit()
        session.refresh(job)

    container = client4.containers.run(
        name=new_job.name+"-"+str(new_job.id),
        image=new_job.container_image, 
        command=new_job.command,
        shm_size="1G",
        detach=True,
        environment={
            "NVIDIA_VISIBLE_DEVICES": "0,1",
        }
    )

    success = container.wait()

    # if error occurs inside the docker
    if success != 0:
        with Session(db.engine) as session:
            # find if the job exists
            job = session.exec(
                select(db.Job)
                .where(col(db.Job.id) == new_job.id)
            ).one()
            job.completed_at = datetime.datetime.now()
            session.commit()
            session.refresh(job)
            
        # save the output in the `output` folder
        with open(f"output/{job.name}_{str(job.id)}.txt", "w") as f:
            # convert the output from bytes to string and write to file
            f.write(container.logs().decode("utf-8"))

    return success

@app.post("/jobs", response_model=Job)
async def add_job(job: Job, background_tasks: BackgroundTasks):
    "Add a job to the scheduler"
    with Session(db.engine) as session:
        job = db.Job(**job.dict())
        session.add(job)
        session.commit()
        session.refresh(job)
    
    # run the job in the background
    # run_horovod.delay(job.id, job.name, job.container_image, job.command)
    background_tasks.add_task(run_docker, job)
    return job


@app.get("/jobs")
async def get_jobs():
    "Get all jobs"
    with Session(db.engine) as session:
        jobs = session.exec(
            select(db.Job)
            .order_by(col(db.Job.created_at), col(db.Job.no_of_gpus).desc())
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


@app.delete("/jobs/{id}")
async def kill_job(id: int):
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
        return job


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=int(config.PORT))
