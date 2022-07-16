from config import log_config
from logging.config import dictConfig
import logging

from fastapi import FastAPI
from pydantic import BaseModel
from sqlmodel import create_engine
from database import InitializeDB

dictConfig(log_config)
logger = logging.getLogger("schedulearn")

InitializeDB(logger)
engine = create_engine("sqlite:///schedulearn.sqlite3", echo=True)
app = FastAPI(debug=True)
logger.info("API is running at http://localhost:5000/")

class Job(BaseModel):
    name: str
    type: str
    image: str
    command: str
    required_gpus: int

# create an endpoint that receives json file
@app.post("/api/v1/post")
async def get_job(job: Job):
    # # insert the job into the database
    # with Session(engine) as session:
    #     session.add(job)
    #     session.commit()
    return job