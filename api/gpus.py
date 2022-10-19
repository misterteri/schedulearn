from dataclasses import dataclass
import subprocess
import csv
from config import SERVERS
@dataclass(frozen=True)
class Gpu:
    server: str
    uuid: str
    id: int
    name: str
    utilization: float

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
