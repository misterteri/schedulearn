import database as db
from dataclasses import dataclass
from sqlmodel import Session, select, col
from lib import get_available_gpus, get_available_gpus_at, get_most_available_gpus

@dataclass
class Destination:
    server: str
    gpus: list[int]

@dataclass
class Scheduler:
    def add_job(self, job):
        pass

    def remove_job(self, job):
        pass
    
    def get_jobs(self, job): # get jobs that are assigned to a specific scheduler
        pass
    
    def kill_job(self, job):
        pass

    def migrate_job(self, job):
        pass
    
    def run_job(self, job):
        pass

@dataclass
class FIFO(Scheduler):
    # Only create variables and functions that specific to FIFO
    pass

@dataclass
class RoundRobin(Scheduler):
    # Only create variables and functions that specific to Round Robin
    pass

@dataclass
class SRJF(Scheduler):
    # Only create variables and functions that specific to SRJF
    pass


# def FIFO(required_gpus: int) -> Destination:
#     destination = Destination(server="", gpus=[])
#     # if destination.server == "", keep until destination.server is not ""
#     while destination.server == "" and destination.server not in ["gpu3", "gpu4", "gpu5"]:
#         destination = get_available_gpus(required_gpus)
#     return destination


# def RoundRobin(required_gpus: int) -> Destination | None:
#     with Session(db.engine) as session:
#         last_server = session.exec(
#             select(db.Schedulearn)
#             .where(col(db.Schedulearn.configuration) == "last_server")
#         ).one()

#     destination = get_available_gpus_at(last_server.value, required_gpus)

#     with Session(db.engine) as session:
#         last_server = session.exec(
#             select(db.Schedulearn)
#             .where(col(db.Schedulearn.configuration) == "last_server")
#         ).one()
#         next_server = session.exec(
#             select(db.Schedulearn)
#             .where(col(db.Schedulearn.configuration) == "next_server")
#         ).one()
#         # update the last server and the next server
#         last_server.value = next_server.value
#         if next_server.value == 'gpu3':
#             next_server.value = 'gpu4'
#         elif next_server.value == 'gpu4':
#             next_server.value = 'gpu5'
#         elif next_server.value == 'gpu5':
#             next_server.value = 'gpu3'
#         session.commit()

#     if len(destination.gpus) < required_gpus:
#         return None
#     return destination