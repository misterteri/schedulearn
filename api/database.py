import uuid
import config
from typing import List
from typing import Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine

engine = create_engine(config.DB_URL, echo=True)

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: Optional[str]
    email: str = Field(max_length=100, default="")
    password: str = Field(max_length=100, default="")
    department: Optional[str]
    degree: Optional[str]
    grade: Optional[int]
    occupation: Optional[str]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    token: Optional[str]
    no_of_logins: int = Field(default=0)


class Job(SQLModel, table=True):
    "Record of a job that has been scheduled"
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(default=None)
    type: str = Field(default=None)
    container_image: str = Field(default=None)
    command: str = Field(default=None)
    trained_at: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    required_gpus: int = Field(default=None)
    weight: int = Field(default=None)
    no_of_migrations: int = Field(default=None)

    running_jobs: List["RunningJob"] = Relationship(back_populates="job")


class Server(SQLModel, table=True):
    "Keeps track of the servers in the cluster"
    id: Optional[int] = Field(primary_key=True, default=None)
    host_name: str = Field()

    gpus: List["Gpu"] = Relationship(back_populates="server")


class Gpu(SQLModel, table=True):
    "Keeps track of the GPU's unique name and the server it is connected to"
    id: Optional[int] = Field(primary_key=True, default=None)
    identifier: str = Field()
    
    server_id: Optional[int] = Field(default=None, foreign_key="server.id")
    server: Optional[Server] = Relationship(back_populates="gpus")


class RunningJob(SQLModel, table=True, table_name="runningjob"):
    "Record of a job that is currently running"
    id: Optional[int] = Field(primary_key=True, default=None)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    weight: int = Field(default=None)
    no_of_migrations: int = Field(default=None)

    job_id: Optional[int] = Field(default=None, foreign_key="job.id")
    gpu_id: Optional[str] = Field(default=None)
    jobs: List["Job"] = Relationship(back_populates="runningjob")
    gpus: List["Gpu"] = Relationship(back_populates="runningjob")


def initialize():
    SQLModel.metadata.create_all(engine)

    # Create a server then add gpus to the server
    with Session(engine) as session:
        for s in config.SERVERS:
            server = Server(host_name=s.host_name)
            session.add(server)
            for g in s.gpus:
                gpu = Gpu(identifier=g.identifier, server=server)
                session.add(gpu)
        session.commit()
