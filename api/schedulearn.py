import uuid
import config
import logging
import datetime
import database as db
from lib import get_docker_client
from logging.config import dictConfig
from scheduler import FIFO, RoundRobin
from sqlmodel import Session, select, col

dictConfig(config.LOGGING)
logger = logging.getLogger(__name__)

def Run(new_job, logger):
    with Session(db.engine) as session:
        scheduling_algorithm = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "algorithm")
        ).first()

    if scheduling_algorithm.value == "FIFO":
        available_gpus = FIFO(new_job.required_gpus)
        logger.info(f"Return {len(available_gpus['gpus'])} with FIFO")

    if scheduling_algorithm.value == "RoundRobin":
        available_gpus = RoundRobin(new_job.required_gpus)
        logger.info(f"Return {len(available_gpus['gpus'])} with RoundRobin")
        
    docker_client = get_docker_client(available_gpus['server'])

    with Session(db.engine) as session:
        job = db.Job(
            name = f"{new_job.name.lower().replace(' ', '-')}-{uuid.uuid4()}",
            type = job.type,
            container_image = job.container_image,
            command = job.command,
            required_gpus = job.required_gpus,
            trained_at = available_gpus['server'],
        )
        
        container = docker_client.containers.run(
            name = job.name,
            image = job.container_image, 
            command = f"horovodrun -np {job.required_gpus} -H localhost:{job.required_gpus} {job.command}",
            shm_size = "1G",
            detach = True,
            environment = {
                "NVIDIA_VISIBLE_DEVICES": f"{','.join([str(gpu) for gpu in available_gpus['gpus']])}",
            }
        )

        job.started_at = datetime.datetime.now()
        session.add(job)
        session.commit()
        session.refresh(job)
        logger.info(f"Job {job.name} added to the database")

        status = container.wait()
        logger.info(f"Container {job.name} created")

        # if error does not occur inside the docker
        if status != 0:
            job.completed_at = datetime.datetime.now()
            session.commit()
            session.refresh(job)
            logger.info(f"Job {job.name} completed")
            with open(f"output/{(job.type).lower()}/{job.container_name}.txt", "w") as f:
                f.write(container.logs().decode("utf-8"))
                logger.info(f"Output of {job.name} saved to file")


def Remove(id, logger):
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()

    docker_client = get_docker_client(job.trained_at)
    container = docker_client.containers.get(job.container_name)

    if container: 
        container.remove()
        logger.info(f"Container {job.container_name} removed")
    else:
        logger.error(f"Container {job.container_name} does not exist")

    session.delete(job)
    session.commit()
    logger.info(f"Job {job.name} removed from the database")