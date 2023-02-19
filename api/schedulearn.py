import uuid
import datetime
import database as db
from lib import get_docker_client
from scheduler import FIFO, RoundRobin
from sqlmodel import Session, select, col
from fastapi import BackgroundTasks

def Run(new_job_id: int, background_tasks: BackgroundTasks):
    with Session(db.engine) as session:
        scheduling_algorithm = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "algorithm")
        ).first()

        new_job = session.exec(
            select(db.Job).where(col(db.Job.id) == new_job_id)
        ).one()

        if scheduling_algorithm.value == "FIFO":
            available_gpus = {'server': None, 'gpus': []}
            while available_gpus['server'] is None or len(available_gpus['gpus']) < new_job.required_gpus:
                found = FIFO(new_job.required_gpus)
                available_gpus['server'] = found['server']
                available_gpus['gpus'] = found['gpus']

        if scheduling_algorithm.value == "RoundRobin":
            available_gpus = RoundRobin(new_job.required_gpus)
        
    docker_client = get_docker_client(available_gpus['server'])

    with Session(db.engine) as session:
        # find the job by new_job.id
        job = session.exec(
            select(db.Job).where(col(db.Job.id) == new_job.id)
        ).one()
        
        job.container_name = f"{new_job.name.lower().replace(' ', '-')}-{uuid.uuid4()}"
        job.trained_at = available_gpus['server']
        job.status = "Running"
        
        container = docker_client.containers.run(
            name = job.container_name,
            image = job.container_image, 
            command = f"horovodrun -np {job.required_gpus} -H localhost:{job.required_gpus} {job.command}",
            shm_size = "1G",
            detach = True,
            environment = {
                "NVIDIA_VISIBLE_DEVICES": f"{','.join([str(gpu) for gpu in available_gpus['gpus']])}",
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
        elif status.get('StatusCode') == 1 or status.get('StatusCode') == 2:
            container = docker_client.containers.get(job.container_name)
            if container:
                container.remove()
                job.container_name = None
                job.completed_at = None
                job.status = "Error"
                session.commit()
                session.refresh(job)
                background_tasks.add_task(Run, job.id, background_tasks)
            else:
                job.container_name = None
                job.completed_at = None
                job.status = "Error"
                session.commit()
                session.refresh(job)
                background_tasks.add_task(Run, job.id, background_tasks)


def Remove(id):
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