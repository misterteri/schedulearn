import csv
import time
import config
import psutil
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


def get_gpus():
    gpus = []
    for server in ['gpu3', 'gpu4', 'gpu5']:
        result = subprocess.run(
            f"ssh {server} nvidia-smi --query-gpu=uuid,gpu_name,utilization.gpu --format=csv,noheader".split(' '), 
            stdout = subprocess.PIPE
        ).stdout.decode('utf-8').splitlines()
        
        for i, stat in enumerate(csv.reader(result, delimiter=',')):
            gpus.append(Gpu(server=server, uuid=stat[0], id=f"{i}", name=stat[1], utilization=float(stat[2].strip('%'))))

    return gpus


def get_gpu_utilization():
    gpus = get_gpus()
    utilizations = {}
    for gpu in gpus:
        utilizations[f"{gpu.server}-{gpu.id}"] = gpu.utilization
    return utilizations


def get_cpu_utilization():
    return psutil.cpu_percent()


def get_ram_utilization():
    return psutil.virtual_memory().percent


def get_docker_client(server: str):
    if server == "gpu3":
        return config.GPU3_DOCKER_CLIENT
    elif server == "gpu4":
        return config.GPU4_DOCKER_CLIENT
    elif server == "gpu5":
        return config.GPU5_DOCKER_CLIENT


def get_scheduler(scheduler: str):
    if scheduler == "FIFO":
        pass
    elif scheduler == "AFSL":
        pass
    elif scheduler == "Tiresias":
        pass


def get_system_status():
    with open('utilization.csv', 'a') as f:
        if f.tell() == 0:
            f.write('time,gpu3-0,gpu3-1,gpu3-2,gpu3-3,gpu4-0,gpu4-1,gpu4-2,gpu4-3,gpu5-0,gpu5-1,gpu5-2,gpu5-3,cpu,ram\n')

        while True:
            gpu_utilization = get_gpu_utilization()
            f.write(f"{datetime.now()},{gpu_utilization['gpu3-0']},{gpu_utilization['gpu3-1']},{gpu_utilization['gpu3-2']},{gpu_utilization['gpu3-3']},{gpu_utilization['gpu4-0']},{gpu_utilization['gpu4-1']},{gpu_utilization['gpu4-2']},{gpu_utilization['gpu4-3']},{gpu_utilization['gpu5-0']},{gpu_utilization['gpu5-1']},{gpu_utilization['gpu5-2']},{gpu_utilization['gpu5-3']},{get_cpu_utilization()},{get_ram_utilization()}\n")
            time.sleep(2)