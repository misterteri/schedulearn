import csv
import config
import docker
import subprocess
from datetime import datetime
from dataclasses import dataclass

@dataclass(frozen=True)
class Gpu:
    server: str
    uuid: str
    id: int
    name: str
    utilization: float
    memory_usage: int
    timestamp: datetime

    def __str__(self):
        return f"{self.server},{self.uuid},{self.id},{self.name},{self.utilization},{self.memory_usage},{self.timestamp}"


def get_docker_client(server: str) -> docker.DockerClient:
    if server == "gpu3":
        return config.GPU3_DOCKER_CLIENT
    elif server == "gpu4":
        return config.GPU4_DOCKER_CLIENT
    elif server == "gpu5":
        return config.GPU5_DOCKER_CLIENT


def get_gpus() -> list[Gpu]:
    gpus = []
    for server in ['gpu3', 'gpu4', 'gpu5']:
        result = subprocess.run(
            f"ssh {server} nvidia-smi --query-gpu=uuid,gpu_name,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits".split(' '), 
            stdout = subprocess.PIPE
        ).stdout.decode('utf-8').splitlines()
        
        for i, stat in enumerate(csv.reader(result, delimiter=',')):
            gpus.append(
                Gpu(
                    server=server, 
                    uuid=stat[0], 
                    id=f"{server}-{i}",
                    name=stat[1], 
                    utilization=float(stat[2].strip('%')), 
                    memory_usage=int(int(stat[3])/int(stat[4])*100),
                    timestamp=datetime.now()
                )
            )
    return gpus


def log_system_status(filename: str) -> None:
    with open(filename, 'a') as f:
        gpus = get_gpus()
        if f.tell() == 0:
            f.write(
                f"time,{','.join([gpu.id for gpu in gpus])}\n"
            )
        else: 
            f.write(
                f"{datetime.now()},{','.join([str(gpu.memory_usage) for gpu in gpus])}\n"
            )