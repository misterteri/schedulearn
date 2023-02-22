import uuid
import datetime
import database as db
from lib import get_docker_client
from scheduler import FIFO, RoundRobin
from sqlmodel import Session, select, col
from fastapi import BackgroundTasks

def migrate_job():
    pass

def scale_in_job():
    pass

def scale_out_job():
    pass

def run_job(new_job_id: int, background_tasks: BackgroundTasks):
    with Session(db.engine) as session:
        scheduling_algorithm = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "algorithm")
        ).first()

        new_job = session.exec(
            select(db.Job).where(col(db.Job.id) == new_job_id)
        ).one()

        if scheduling_algorithm.value == "FIFO":
            available_resources = {'server': None, 'gpus': []}
            while available_resources['server'] is None or len(available_resources['gpus']) < new_job.required_gpus:
                found = FIFO(new_job.required_gpus)
                available_resources['server'] = found['server']
                available_resources['gpus'] = found['gpus']
        
        if scheduling_algorithm.value == "ElasticFIFO":
            available_resources = {'server': None, 'gpus': []}
            for server in ["gpu3", "gpu4", "gpu5"]:
                found = FIFO(new_job.required_gpus, server)
                available_resources['server'] = found['server'] if found['server'] is not None else available_resources['server']
                available_resources['gpus'] = found['gpus'] if found['gpu'] is not None else available_resources['gpus']
            
            if found['server'] is not None and len(found['gpus']) >= new_job.required_gpus:
                # 1. Get the server with the highest avg. GPU utilization
                busiest_server = ... # e.g. 'gpu3'
                # 2. Find the job with the most number of GPUs
                job_with_most_gpus = ... 
                # 3. Get the ids of GPUs where the busiest job was running
                released_gpus = ... # e.g. [1, 2, 3]
                # 4. Scale in the job
                scale_in_job(job_with_most_gpus)
                available_resources['server'] = busiest_server
                available_resources['gpus'] = released_gpus

        if scheduling_algorithm.value == "RoundRobin":
            available_resources = RoundRobin(new_job.required_gpus)
        
    docker_client = get_docker_client(available_resources['server'])

    with Session(db.engine) as session:
        # find the job by new_job.id
        job = session.exec(
            select(db.Job).where(col(db.Job.id) == new_job.id)
        ).one()
        
        job.container_name = f"{new_job.name.lower().replace(' ', '-')}-{uuid.uuid4()}"
        job.trained_at = available_resources['server']
        job.status = "Running"
        
        container = docker_client.containers.run(
            name = job.container_name,
            image = job.container_image, 
            command = f"horovodrun -np {job.required_gpus} -H localhost:{job.required_gpus} {job.command}",
            shm_size = "1G",
            detach = True,
            environment = {
                "NVIDIA_VISIBLE_DEVICES": f"{','.join([str(gpu) for gpu in available_resources['gpus']])}",
            }
        )

        job.started_at = datetime.datetime.now()
        session.commit()
        session.refresh(job)

        status = container.wait()

        if status.get('StatusCode') == 0:
            job.completed_at = datetime.datetime.now()
            job.status = "Completed"
            session.commit()
            session.refresh(job)
            with open(f"output/{(job.type).lower()}/{job.container_name}.txt", "w") as f:
                f.write(container.logs().decode("utf-8"))
            
            scheduling_algorithm = session.exec(
                select(db.Schedulearn)
                .where(col(db.Schedulearn.configuration) == "algorithm")
            ).first()

            if scheduling_algorithm.value == "ElasticFIFO":
                # 1. Get the slowest and unfinished job
                slowest_unfinished_job = ...
                # 2. Scale out the job
                scale_out_job(slowest_unfinished_job)
        elif status.get('StatusCode') == 1 or status.get('StatusCode') == 2:
            container = docker_client.containers.get(job.container_name)
            if container:
                container.remove()
                job.container_name = None
                job.completed_at = None
                job.status = "Error"
                session.commit()
                session.refresh(job)
                background_tasks.add_task(run_job, job.id, background_tasks)
            else:
                job.container_name = None
                job.completed_at = None
                job.status = "Error"
                session.commit()
                session.refresh(job)
                background_tasks.add_task(run_job, job.id, background_tasks)


def remove_job(id):
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()

    docker_client = get_docker_client(job.trained_at)
    container = docker_client.containers.get(job.container_name)

    if container: 
        container.remove()
    else:
        return

    session.delete(job)
    session.commit()