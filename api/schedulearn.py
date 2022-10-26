import datetime
import database as db
from scheduler import FIFO, RoundRobin
from sqlmodel import Session, select, col
from lib import get_docker_client
import uuid


def Run(new_job):
    with Session(db.engine) as session:
        scheduling_algorithm = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "algorithm")
        ).first()

    if scheduling_algorithm.value == "FIFO":
        available_gpus = FIFO(new_job.required_gpus)

    if scheduling_algorithm.value == "RoundRobin":
        available_gpus = RoundRobin(new_job.required_gpus)
        
    docker_client = get_docker_client(available_gpus['server'])

    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == new_job.id)
        ).one()
        job.name = new_job.name
        job.container_name = f"{new_job.name}-{uuid.uuid4()}".lower().replace(" ", "-")
        job.container_image = new_job.container_image
        job.required_gpus = new_job.required_gpus
        job.command = new_job.command
        job.trained_at = available_gpus['server']
        job.started_at = datetime.datetime.now()

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

        status = container.wait()

        # if error does not occur inside the docker
        if status != 0:
            job.completed_at = datetime.datetime.now()
            session.commit()
            session.refresh(job)
            # save the output in the `output` folder
            with open(f"output/{job.name}.txt", "w") as f:
                # convert the output from bytes to string and write to file
                f.write(container.logs().decode("utf-8"))
            return status


def Remove(id):
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()

        docker_client = get_docker_client(job.trained_at)

        # kill the container running the job
        container = docker_client.containers.get(job.container_name)

        if container:
            # container.kill()
            container.remove()
        
        # delete the job from the database
        session.delete(job)
        session.commit()