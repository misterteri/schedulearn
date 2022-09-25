from dataclasses import dataclass
import subprocess
import csv


@dataclass(frozen=True)
class Gpu:
    server: str
    uuid: str
    id: int
    name: str
    utilization: float


SERVERS = ['gpu3', 'gpu4', 'gpu5']


def fetch_all_gpus():
    gpus = []
    for server in SERVERS:
        result = subprocess.run(
            f"ssh {server} nvidia-smi --query-gpu=uuid,gpu_name,utilization.gpu --format=csv,noheader".split(' '), 
            stdout = subprocess.PIPE
        ).stdout.decode('utf-8').splitlines()
        
        for i, stat in enumerate(csv.reader(result, delimiter=',')):
            gpus.append(Gpu(server=server, uuid=stat[0], id=f"{i}", name=stat[1], utilization=float(stat[2].strip('%'))))

    return gpus


def fetch_available_gpus(required_gpus: int) -> dict | None:
    gpus = fetch_all_gpus()
    for server in SERVERS:
        available = [gpu for gpu in gpus if gpu.server == server and gpu.utilization < 90]
        if len(available) >= required_gpus:
            # return a dictionary with server and gpu ids
            result = {'server': server, 'id': []}
            for gpu in available[:required_gpus]:
                result['id'].append(gpu.id)
            return result