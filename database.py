import os
import logging
from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, create_engine, Session

DB_FILE = "schedulearn.sqlite3"
engine = create_engine(f"sqlite:///{DB_FILE}", echo=True)

GPU_ID = [0,1,2,3]
SERVERS = ["gpu3", "gpu4", "gpu5"]

class Job(SQLModel, table = True, table_name="jobs"):
    id: int = Field(primary_key=True)
    job_name: str = Field(default=None)
    job_type: str = Field(default=None)
    container_image: str = Field(default=None)
    command: str = Field(default=None)
    created_at: datetime = Field(default=None)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    required_gpus: int = Field(default=None)
    weight: int = Field(default=None)
    number_of_migrations: int = Field(default=None)
    at_server: list[str] = Field(default=None, foreign_key="servers.id")

class Server(SQLModel, table = True, table_name="servers"):
    id: str = Field(primary_key=True, nullable=False)
    occupied_at: Optional[int] = Field(default=None, foreign_key="gpus.id")

class Gpu(SQLModel, table = True, table_name="gpus"):
    id: str = Field(primary_key=True, nullable=False)
    server_id: Optional[str] = Field(foreign_key="servers.id", nullable=False)
    job_id: Optional[str] = Field(foreign_key="jobs.id")

def create_tables():
    SQLModel.metadata.create_all(engine)

def InitializeDB(logger: logging.Logger):
    if not os.path.exists(DB_FILE):
        create_tables()

        # populate servers
        with Session(engine) as session:
            for server in SERVERS:
                session.add(Server(id=server))
                logger.info(f"Created server {server}")
            session.commit()

        # populate gpus
        with Session(engine) as session:
            for server in SERVERS:
                for gpu in GPU_ID:
                    session.add(Gpu(id=f"{server}-{gpu}", server_id=server))
                    logger.info(f"Created gpu {gpu} on server {server}")
            session.commit()