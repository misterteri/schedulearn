import uuid
import config
import logging
import database as db
from fastapi import BackgroundTasks
from datetime import datetime
from dataclasses import dataclass
from logging.config import dictConfig
from sqlmodel import Session,select, col
from lib import get_docker_client, get_most_available_gpus, get_available_gpus, get_available_gpus_at

dictConfig(config.LOGGING)
logger = logging.getLogger(__name__)

@dataclass
class Destination:
    server: str
    gpus: list[int]
    required_gpus: int

@dataclass
class Job:
    id: int
    name: str
    type: str
    container_name: str
    container_image: str
    command: str
    created_at: datetime
    started_at: datetime
    completed_at: datetime
    estimated_completion_time: datetime
    required_gpus: int
    no_of_migrations: int
    trained_at: str

class Scheduler:
    @staticmethod
    def add_job(self, job: Job):
        with Session(db.engine) as session:
            new_job = db.Job(
                name = job.name,
                type = job.type,
                container_name = job.container_name,
                container_image = job.container_image,
                command = job.command,
                created_at = datetime.now(),
                required_gpus = job.required_gpus,
                no_of_migrations = 0,
                trained_at = None
            )
            session.add(new_job)
            session.commit()
            session.refresh(new_job)
            logger.info(f"Job {new_job.name} added to the scheduler")

    @staticmethod
    def remove_job(self, job:Job):
        with Session (db.engine) as session:
            job = session.exec(
                select(job)
                .where(col(job.id) == job.id)
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
    
    @staticmethod
    def get_jobs(self, job:Job):
        # get jobs that are assigned to a specific scheduler
        with Session(db.engine) as session:
            jobs = session.exec(
                select(db.Job)
                .where(col(db.Job.trained_at) == job.trained_at)
                .where(col(db.Job.completed_at) == None)
            ).all()
        return jobs
    
    @staticmethod
    def kill_job(self, job:Job):
        with Session(db.engine) as session:
            job = session.exec(
                select(db.Job)
                .where(col(db.Job.id) == job.id)
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

    @staticmethod
    def estimate_job_duration(self, job:Job):
        with Session (db.engine) as session:
            similar_jobs = session.exec(
                select(db.Job)
                .where(col(db.Job.type) == job.type)
                .where(col(db.Job.completed_at) != None)
            ).all()
            avg_duration = 0

        for similar_job in similar_jobs:
            if similar_job.estimated_completion_time and similar_job.started_at:
                avg_duration += (similar_job.estimated_completion_time - similar_job.started_at).seconds

        avg_duration = avg_duration / len(similar_jobs)
        logger.info(f"Estimated duration of {job.name} is {avg_duration} seconds")
        return avg_duration if avg_duration else 300

    @staticmethod
    def migrate_job(self, job:Job, background_tasks: BackgroundTasks):
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

        # TODO: fix this later
        background_tasks.add_task(self.run_job, job, destination, background_tasks)
    
    def run_job(self, job: Job, background_tasks: BackgroundTasks, destination: Destination):
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
            job.estimated_completion_time = datetime.datetime.now() + datetime.timedelta(seconds=self.estimate_job_duration(job))
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
                background_tasks.add_task(self.autoscale, background_tasks)
            elif status.get('StatusCode') == 1:
                logger.info(f"Container {job.name}: [Errno 1] Application error")
                container.remove()
                background_tasks.add_task(self.autoscale, background_tasks)
            elif status.get('StatusCode') == 2:
                logger.info(f"Container {job.name}: [Errno 2] No such file or directory")
                container.remove()
                background_tasks.add_task(self.autoscale, background_tasks)

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
                background_tasks.add_task(self.autoscale, background_tasks)
                # background_tasks.add_task(self.run_job, job, destination, background_tasks) # Only one job was migrated 13 times

    @staticmethod
    def autoscale(self, job: Job, background_tasks: BackgroundTasks):
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
                self.kill_job(slowest_job.id)
                background_tasks.add_task(self.migrate_job, slowest_job.id, background_tasks)

@dataclass
class FIFO(Scheduler):
  def FIFO(self, destination:Destination):
    destination = Destination(server="", gpus=[])
    while destination.server == "" and destination.server not in ["gpu3", "gpu4", "gpu5"]:
        destination = get_available_gpus(destination.required_gpus)
    return destination
    
@dataclass
class RoundRobin(Scheduler):
    def RoundRobin(self, destination:Destination):
        with Session(db.engine) as session:
            last_server = session.exec(
                select(db.Schedulearn)
                .where(col(db.Schedulearn.configuration) == "last_server")
            ).one()

        destination = get_available_gpus_at(last_server.value, destination.required_gpus)

        with Session(db.engine) as session:
            last_server = session.exec(
                select(db.Schedulearn)
                .where(col(db.Schedulearn.configuration) == "last_server")
            ).one()
            next_server = session.exec(
                select(db.Schedulearn)
                .where(col(db.Schedulearn.configuration) == "next_server")
            ).one()
            # update the last server and the next server
            last_server.value = next_server.value
            if next_server.value == 'gpu3':
                next_server.value = 'gpu4'
            elif next_server.value == 'gpu4':
                next_server.value = 'gpu5'
            elif next_server.value == 'gpu5':
                next_server.value = 'gpu3'
            session.commit()

        if len(destination.gpus) < destination.required_gpus:
            return None
        return destination

class SRJF(Scheduler):
# Only create variables and functions that specific to SRJF
    pass