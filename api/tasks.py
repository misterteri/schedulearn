from celery import Celery
import docker
import datetime
import database as db
from sqlmodel import Session, select, col
import config

app = Celery('tasks', broker='amqp://guest@localhost//')
client3 = docker.from_env()
client4 = docker.DockerClient(
    base_url=config.GPU4_DOCKER_HOST,
    use_ssh_client=True,
    tls=True,
)
client5 = docker.DockerClient(
    base_url=config.GPU5_DOCKER_HOST,
    use_ssh_client=True,
    tls=True
)

@app.task
def run_horovod(id: int, name: str, image: str, command: str):
    with Session(db.engine) as session:
        job = session.exec(
            select(db.Job)
            .where(col(db.Job.id) == id)
        ).one()
        job.started_at = datetime.datetime.now()
        session.commit()
        session.refresh(job)

    container = client4.containers.run(
        name=name+"_"+str(id),
        image=image, 
        command=command,
        shm_size="1G",
        detach=True,
        environment={
            "NVIDIA_VISIBLE_DEVICES": "0,1",
        }
    )

    success = container.wait()

    # if error occurs inside the docker
    if success != 0:
        with Session(db.engine) as session:
            # find if the job exists
            job = session.exec(
                select(db.Job)
                .where(col(db.Job.id) == id)
            ).one()
            job.completed_at = datetime.datetime.now()
            session.commit()
            session.refresh(job)
            
        # save the output in the `output` folder
        with open(f"output/{name}_{str(id)}.txt", "w") as f:
            # convert the output from bytes to string and write to file
            f.write(container.logs().decode("utf-8"))

        return job
