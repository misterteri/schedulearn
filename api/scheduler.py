from gpus import fetch_all_gpus
from config import SERVERS

def FIFO(required_gpus: int) -> dict | None:
    gpus = fetch_all_gpus()
    for server in SERVERS:
        available = [gpu for gpu in gpus if gpu.server == server and gpu.utilization < 90]
        if len(available) >= required_gpus:
            # return a dictionary with server and gpu ids
            result = {'server': server, 'gpus': []}
            for gpu in available[:required_gpus]:
                result['gpus'].append(gpu.id)
            return result
    return 

def AFSL():
    pass

def Tiresias():
    pass