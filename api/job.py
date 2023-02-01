import uuid
import config
import logging
import datetime
import database as db
from dataclasses import dataclass
from fastapi import BackgroundTasks
from logging.config import dictConfig
from sqlmodel import Session, select, col
from lib import get_docker_client, get_most_available_gpus

dictConfig(config.LOGGING)
logger = logging.getLogger(__name__)

@dataclass
class Destination:
    server: str
    gpus: list[int]


def run_job(job: db.Job, destination: Destination, background_tasks: BackgroundTasks):
    docker_client = get_docker_client(destination.server)

    with Session(db.engine) as session:
        job = session.exec(select(db.Job).where(col(db.Job.id) == job.id)).first()
        # if job.completed_at has value, it means that the job has been completed
        if job.completed_at:
            return
        container_name = f"{job.name.lower().replace(' ', '-')}-{uuid.uuid4()}"
        container = docker_client.containers.run(
            name = container_name,
            image = job.container_image, 
            command = f"horovodrun -np {job.required_gpus} -H localhost:{job.required_gpus} {job.command}",
            shm_size = "1G",
            detach = True,
            environment = {
                # "NVIDIA_VISIBLE_DEVICES": f"{','.join([str(gpu) for gpu in destination.gpus])}",
                "NVIDIA_VISIBLE_DEVICES": "all",
            }
        )
        job.container_name = container_name
        job.trained_at = destination.server
        job.started_at = datetime.datetime.now()
        job.estimated_completion_time = datetime.datetime.now() + datetime.timedelta(seconds=estimate_job_duration(job))
        session.commit()
        session.refresh(job)
        status = container.wait()

        # if error does not occur inside the docker
        if status.get('StatusCode') == 0:
            job.completed_at = datetime.datetime.now()
            session.commit()
            session.refresh(job)
            logger.info(f"Job {job.name} completed")
            with open(f"output/{(job.type).lower()}/{job.container_name}.txt", "w") as f:
                f.write(container.logs().decode("utf-8"))
                logger.info(f"Output of {job.name} saved to file")
            background_tasks.add_task(autoscale, background_tasks)
        elif status.get('StatusCode') == 1:
            logger.info(f"Container {job.name}: [Errno 1] Application error")
            container.remove()
            background_tasks.add_task(autoscale, background_tasks)
        elif status.get('StatusCode') == 2:
            logger.info(f"Container {job.name}: [Errno 2] No such file or directory")
            container.remove()
            background_tasks.add_task(autoscale, background_tasks)

        # check if there is job that is not completed
        # if there is, run the job
        uncompleted_jobs = session.exec(
            select(db.Job)
            .where(col(db.Job.completed_at) == None)
        ).all()

        # if uncompleted_jobs is empty
        if not uncompleted_jobs:
            logger.info("No uncompleted job found")
            return

        for _ in uncompleted_jobs:
            # Try this code first
            # If none of the jobs are migrated, then try the other code
            background_tasks.add_task(autoscale, background_tasks)
            # background_tasks.add_task(run_job, job, destination, background_tasks) # Only one job was migrated 13 times


def estimate_job_duration(job: db.Job):
    """
        Estimate the duration of a job in seconds.
    """
    with Session(db.engine) as session:
        similar_jobs = session.exec(
            select(db.Job)
            .where(col(db.Job.type) == job.type)
            .where(col(db.Job.required_gpus) == job.required_gpus)
            .where(col(db.Job.name).like(f"{job.name}"))
        ).all()

        avg_duration = 0

        for similar_job in similar_jobs:
            if similar_job.estimated_completion_time and similar_job.started_at:
                avg_duration += (similar_job.estimated_completion_time - similar_job.started_at).seconds

        avg_duration = avg_duration / len(similar_jobs)
        logger.info(f"Estimated duration of {job.name} is {avg_duration} seconds")
        return avg_duration if avg_duration else 300


def remove_job(id: int):
    """
        Remove a job with the given id from the 
        database and from the training server.
    """
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


def kill_job(id):
    """
        Kill a job with the given id without 
        removing the job from the database.
    """
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
            .where(col(db.Job.completed_at) == None)
        ).one()

        docker_client = get_docker_client(job.trained_at)
        # get a list of all containers
        containers = docker_client.containers.list(all=True)

        # if the job.container_name not in the list of containers, return
        if job.container_name not in [container.name for container in containers]:
            logger.info(f"Container {job.container_name} does not exist")
            return
        else:
            container = docker_client.containers.get(job.container_name)
            container.stop()
            container.remove()
            logger.info(f"Container {job.container_name} stopped and removed")

            job.trained_at = None
            session.commit()
            session.refresh(job)
            logger.info(f"Job {job.name} killed")


def migrate_job(id: int, background_tasks: BackgroundTasks):
    """
        Move a job from one server to another.
        This function takes two parameters:
        1. id: the id of the job to be moved
        2. destination: the server to move the job to
    """
    destination = get_most_available_gpus()
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()

        # update the job required gpus to the number of gpus available on the destination server
        job.required_gpus = len(destination.gpus)
        job.container_name = f"{job.name}-{job.no_of_migrations}"
        job.no_of_migrations = job.no_of_migrations + 1
        session.commit()
        session.refresh(job)
        logger.info(f"Job {job.name} metadata updated")
    logger.info(f"Job {job.name} migrated to {destination.server}")
    background_tasks.add_task(run_job, job, destination, background_tasks)


def autoscale(background_tasks: BackgroundTasks):
    """
        Initiate migration of jobs to other servers.
        Migration is killing a job and rescheduling it on another server with more resources.
        This function is called every 1 minutes or when a job is finished.
    """

    with Session(db.engine) as session:
        slowest_jobs = session.exec(
            select(db.Job)
            .where(col(db.Job.started_at) != None) # The job has started
            .where(col(db.Job.completed_at) == None) # The job has not completed
            .order_by(col(db.Job.started_at).asc()) # Order the job from the oldest to the newest
        ).all() # return many uncompleted jobs
        
        if slowest_jobs == []:
            return
        else:
            slowest_job = slowest_jobs[0] # Pick the job with the oldest start time
            if (slowest_job.estimated_completion_time - datetime.datetime.now()).seconds < 120:
                return
            kill_job(slowest_job.id)
            background_tasks.add_task(migrate_job, slowest_job.id, background_tasks)