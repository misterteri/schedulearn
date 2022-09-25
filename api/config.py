from dataclasses import dataclass
import os
from typing import List
import docker
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv("PORT") or 5000
DB_URL = os.getenv("DB_URL") or "sqlite:///database.db"

GPU3_DOCKER_HOST = f"ssh://{os.environ.get('USERNAME')}@{os.environ.get('GPU3_IP')}"
GPU4_DOCKER_HOST = f"ssh://{os.environ.get('USERNAME')}@{os.environ.get('GPU4_IP')}"
GPU5_DOCKER_HOST = f"ssh://{os.environ.get('USERNAME')}@{os.environ.get('GPU5_IP')}"

SECRET = "SUPER_STRONG_SECRET"

GPU3_DOCKER_CLIENT = docker.DockerClient(
    base_url=GPU3_DOCKER_HOST,
    use_ssh_client=True,
    tls=True,
)

GPU4_DOCKER_CLIENT = docker.DockerClient(
    base_url=GPU4_DOCKER_HOST,
    use_ssh_client=True,
    tls=True,
)

GPU5_DOCKER_CLIENT = docker.DockerClient(
    base_url=GPU5_DOCKER_HOST,
    use_ssh_client=True,
    tls=True
)

@dataclass
class Gpu:
    "Keeps track of the GPU's unique name and the server it is connected to"
    identifier: str

@dataclass
class Server:
    "Keeps track of the servers in the cluster"
    host_name: str
    gpus: List[Gpu]

SERVERS = [
    Server(
        host_name="gpu3", 
        gpus=[ 
            Gpu(identifier="gpu3-0"), 
            Gpu(identifier="gpu3-1"),
            Gpu(identifier="gpu3-2"), 
            Gpu(identifier="gpu3-3")
        ]
    ),
    Server(
        host_name="gpu4", 
        gpus=[ 
            Gpu(identifier="gpu4-0"), 
            Gpu(identifier="gpu4-1"), 
            Gpu(identifier="gpu4-2"), 
            Gpu(identifier="gpu5-3")
        ]
    ),
    Server(
        host_name="gpu5", 
        gpus=[ 
            Gpu(identifier="gpu5-0"), 
            Gpu(identifier="gpu5-1"), 
            Gpu(identifier="gpu5-2"), 
            Gpu(identifier="gpu5-3")
        ]
    ),
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s | %(asctime)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    "loggers": {
        "schedulearn": {"handlers": ["default"], "level": "DEBUG"},
    }
}
