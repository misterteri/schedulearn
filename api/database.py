import config
from lib import get_gpus
from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel, Session, create_engine, select

engine = create_engine(config.DB_URL, echo=True)

class Schedulearn(SQLModel, table=True):
    configuration: Optional[str] = Field(default="RoundRobin", primary_key=True)
    value: Optional[str]

class Server(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    host_name: str = Field(default=None)

    jobs: List["Job"] = Relationship(back_populates="server")
    gpus: List["Gpu"] = Relationship(back_populates="server")


class Gpu(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    uuid: str = Field(default=None)
    identifier: str = Field(default=None)
    name: str = Field(default=None)

    jobs: List["Job"] = Relationship(back_populates="gpu")

    server_id: Optional[int] = Field(default=None, foreign_key="server.id")
    server: Optional["Server"] = Relationship(back_populates="gpus")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
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
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(default=None)
    type: str = Field(default=None)
    container_name: str = Field(default=None)
    container_image: str = Field(default=None)
    command: str = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    estimated_completion_time: Optional[datetime] = Field(default=None)
    required_gpus: int = Field(default=None)
    no_of_migrations: int = Field(default=None)
    server_id: Optional[int] = Field(default=None, foreign_key="server.id")
    server: Optional[Server] = Relationship(back_populates="gpus")

    gpu_id: Optional[int] = Field(default=None, foreign_key="gpu.id")
    gpu: Optional[Gpu] = Relationship(back_populates="jobs")


def create_tables():
    SQLModel.metadata.create_all(engine)

def create_servers():
    all_gpus = get_gpus()
    SERVERS = list(set([gpu.server for gpu in all_gpus]))  

    with Session(engine) as session:
        for server in SERVERS:
            if not session.exec(select(Server).where(Server.host_name == server)).first():
                session.add(Server(host_name=server))
        session.commit()

def create_gpus():
    all_gpus = get_gpus()

    with Session(engine) as session:
        servers = session.exec(select(Server)).all()
        for server in servers:
            gpus = [gpu for gpu in all_gpus if gpu.server == server.host_name]
            for gpu in gpus:
                if not session.exec(select(Gpu).where(Gpu.identifier == f"{server.host_name}-{gpu.id}")).first():
                    session.add(
                        Gpu(
                            uuid=gpu.uuid,
                            identifier=f"{server.host_name}-{gpu.id}",
                            name=gpu.name,
                            server_id=server.id,
                            server=server
                        )
                    )
        session.commit()

def close():
    engine.dispose()