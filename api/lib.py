import csv
import config
import docker
import subprocess
from datetime import datetime
from dataclasses import dataclass
import concurrent.futures


@dataclass
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

@dataclass
class Destination:
    server: str
    gpus: list[Gpu]


def get_docker_client(server: str) -> docker.DockerClient:
    """
        Returns a docker client for the specified server.

        Args:
            server (str): The name of the server

        Return:
            docker.DockerClient: A docker client for the specified server
    """
    if server == "gpu3":
        return config.GPU3_DOCKER_CLIENT
    elif server == "gpu4":
        return config.GPU4_DOCKER_CLIENT
    elif server == "gpu5":
        return config.GPU5_DOCKER_CLIENT


def get_gpus() -> list[Gpu]:
<<<<<<< Updated upstream
    """
        Iterate through each server and returns a list of all graphics cards across all servers.

        Args:
            None
        
        Return:
            A list containing object of GPU class with the following structure.
    """
    gpus: list[Gpu] = []
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
                    id=f"{i}",
                    name=stat[1], 
                    utilization=float(stat[2].strip('%')), 
                    memory_usage=int(int(stat[3])/int(stat[4])*100),
                    timestamp=datetime.now()
=======
    gpus = []
    servers = ['gpu3', 'gpu4', 'gpu5']
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit SSH requests for all servers asynchronously
        futures = {executor.submit(get_gpu_stats, server): server for server in servers}

        # Wait for all SSH requests to complete and process results
        for future in concurrent.futures.as_completed(futures):
            server = futures[future]
            result = future.result()
            
            for i, stat in enumerate(csv.reader(result, delimiter=',')):
                gpus.append(
                    Gpu(
                        server=server, 
                        uuid=stat[0], 
                        id=f"{i}",
                        name=stat[1][1:],
                        utilization=float(stat[2].strip('%')), 
                        memory_usage=int(int(stat[3])/int(stat[4])*100),
                        timestamp=datetime.now()
                    )
>>>>>>> Stashed changes
                )
    return gpus

def get_available_gpus(required_gpus: int) -> Destination:
    """
        Iterate through each server and returns the first server found with the most GPUs

        Args:
            required_gpus (int): The number of GPUs required for the job
        
        Returns:
            Destination: An object of Destination class
            Destination.server: The name of the destination server
            Destination.gpus: A list of IDs of available GPUs at the destination server
    """
    destination = Destination(server="", gpus=[])
    for server in ['gpu3', 'gpu4', 'gpu5']:
        available_gpus = []
        for gpu in get_gpus():
            if gpu.server == server and gpu.memory_usage < 50:
                available_gpus.append(gpu)
        # Get the first server seen with enough available GPUs
        if len(available_gpus) == required_gpus:
            destination.server = server
            destination.gpus = [gpu.id for gpu in available_gpus]
            break
    return destination


def get_most_available_gpus() -> Destination:
    """
        Iterate through all servers and returns the server with the most GPUs

        Args:
            None

        Returns:
            Destination: An object of Destination class
            Destination.server: The name of the destination server
            Destination.gpus: A list of IDs of available GPUs at the destination server
    """
    destination = Destination(server="", gpus=[])
    for server in ['gpu3', 'gpu4', 'gpu5']:
        available_gpus = []
        for gpu in get_gpus():
            if gpu.server == server and gpu.memory_usage < 50:
                available_gpus.append(gpu)
        # Get the server with the most available GPUs
        if len(available_gpus) > len(destination.gpus):
            destination.server = server
            destination.gpus = [gpu.id for gpu in available_gpus]
    return destination


def get_available_gpus_at(destination_server: str, required_gpus: int | None) -> Destination:
    """
        Acquire a list of available GPUs at the specified destination server.

        Args:
            destination_server (str): The name of the destination server
            required_gpus (int | None): The number of GPUs required for the job
        
        Return:
            Destination: An object of Destination class
            Destination.server: The name of the destination server
            Destination.gpus: A list of IDs of available GPUs at the destination server
    """
    destination = Destination(server=destination_server, gpus=[])
    for gpu in get_gpus():
        if gpu.server == destination_server and gpu.memory_usage < 50 and len(destination.gpus) < required_gpus:
            destination.gpus.append(gpu.id)
    return destination


<<<<<<< Updated upstream
def log_system_status(filename: str) -> None:
    """
        Write the system status to a file.

        Args:
            filename (str): The name of the file to write to

        Return:
            None
    """
    with open(filename, 'a') as f:
        gpus = get_gpus()
        if f.tell() == 0:
            f.write(
                f"time,{','.join([f'{gpu.server}-{gpu.id}' for gpu in gpus])}\n"
            )
        else: 
            f.write(
                f"{datetime.now()},{','.join([str(gpu.memory_usage) for gpu in gpus])}\n"
            )
=======
def get_gpu_stats(server):
    return subprocess.run(
        f"ssh {server} nvidia-smi --query-gpu=uuid,gpu_name,utilization.gpu,memory.used,memory.total --format=csv,noheader,nounits".split(' '), 
        stdout=subprocess.PIPE
    ).stdout.decode('utf-8').splitlines()


def get_busiest_server():
    gpus = get_gpus()
    return sorted(gpus, key=lambda gpu: gpu.utilization, reverse=True)[0].server


def get_least_busy_server():
    gpus = get_gpus()
    return sorted(gpus, key=lambda gpu: gpu.utilization)[0].server


# def log_system_status(filename: str) -> None:
#     with open(filename, 'a') as f:
#         gpus = get_gpus()
#         if f.tell() == 0:
#             f.write(
#                 f"time,{','.join([gpu.id for gpu in gpus])}\n"
#             )
#         else: 
#             f.write(
#                 f"{datetime.now()},{','.join([str(gpu.memory_usage) for gpu in gpus])}\n"
#             )


# async def log_system_status(filename: str) -> None:
#     gpus = get_gpus()
#     header = ','.join([gpu.id for gpu in gpus])
#     now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     data = ','.join([str(gpu.memory_usage) for gpu in gpus])
#     content = f"{now},{data}\n"
#     async with aiofiles.open(filename, mode='a') as f:
#         file_size = await f.tell()
#         if file_size == 0:
#             await f.write(f"time,{header}\n")
#         await f.write(content)
>>>>>>> Stashed changes
