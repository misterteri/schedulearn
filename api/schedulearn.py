import datetime
import database as db
from gpus import fetch_available_gpus 
from sqlmodel import Session, select, col
from lib import get_docker_client

def Run(new_job):
    available_gpus = fetch_available_gpus(new_job.required_gpus)
    docker_client = get_docker_client(available_gpus['server'])

    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == new_job.id)
        ).one()
        job.name = f"{new_job.name}-{new_job.id}".lower().replace(" ", "-")
        job.container_image = new_job.container_image
        job.required_gpus = new_job.required_gpus
        job.command = new_job.command
        job.trained_at = available_gpus['server']
        job.started_at = datetime.datetime.now()
        session.commit()
        session.refresh(job)

    container = docker_client.containers.run(
        name = job.name,
        image = job.container_image, 
        command = f"horovodrun -np {job.required_gpus} -H localhost:{job.required_gpus} {job.command}",
        shm_size = "1G",
        detach = True,
        environment = {
            "NVIDIA_VISIBLE_DEVICES": ",".join(available_gpus['gpus']),
        }
    )

    success = container.wait()

    # if error occurs inside the docker
    if success != 0:
        with Session(db.engine) as session:
            # find if the job exists
            job = session.exec(
                select(db.Job)
                .where(col(db.Job.id) == new_job.id)
            ).one()
            job.completed_at = datetime.datetime.now()
            session.commit()
            session.refresh(job)
            
        # save the output in the `output` folder
        with open(f"output/{job.name}.txt", "w") as f:
            # convert the output from bytes to string and write to file
            f.write(container.logs().decode("utf-8"))
        return success

def Remove(id):
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()

        docker_client = get_docker_client(job.trained_at)

        # kill the container running the job
        container = docker_client.containers.get(job.name)

        if container:
            container.kill()
            container.remove()
        
        # delete the job from the database
        session.delete(job)
        session.commit()
        return job