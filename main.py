import logging
from logging.config import dictConfig
from typing import Optional

import config
import database as db
from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import Session, select
import uvicorn

dictConfig(config.LOGGING)

logger = logging.getLogger("schedulearn")
app = FastAPI(debug=True)

class Job(BaseModel):
    name: str
    type: str
    container_image: str
    command: str
    no_of_gpus: int

@app.on_event("startup")
def on_startup():
    db.initialize()


@app.put("/jobs")
async def add_job(job: Job):
    "Add a job to the scheduler"
    with Session(db.engine) as session:
        job = db.Job(**job.dict())
        session.add(job)
        session.commit()
    return job


@app.get("/jobs")
async def get_jobs():
    "Get all jobs"
    with Session(db.engine) as session:
        statement = select(db.Job)
        jobs = session.exec(statement).fetchall()
        return jobs


@app.get("/jobs/{id}")
async def get_job(id: int):
    "Get status of a job"
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job).where(db.Job.id == id)
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
            select(db.Job).where(db.Job.id == id)
        ).one()

        # kill the container running the job
        # ....

        # delete the job from the database
        session.delete(job)
        session.commit()
        return job


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.PORT)
