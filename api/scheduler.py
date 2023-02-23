import database as db
from dataclasses import dataclass
from sqlmodel import Session, select, col
from lib import get_available_gpus, get_available_gpus_at, get_most_available_gpus

<<<<<<< HEAD
@dataclass
class Destination:
    server: str
    gpus: list[int]
=======
def FIFO(required_gpus: int) -> dict | None:
    gpus = get_gpus()

    for server in ['gpu3', 'gpu4', 'gpu5']:
        available_resources = [gpu for gpu in gpus if gpu.server == server and gpu.utilization < 90]
        if len(available_resources) >= required_gpus:
            result = {'server': server, 'gpus': []}
            for gpu in available_resources[:required_gpus]:
                result['gpus'].append(gpu.id)
            return result
    return {'server': None, 'gpus': []}
>>>>>>> 131ffc4ddd559a59ab56f83a9e5bd76fba0b6e37


def FIFO(required_gpus: int) -> Destination:
    destination = Destination(server="", gpus=[])
    # if destination.server == "", keep until destination.server is not ""
    while destination.server == "" and destination.server not in ["gpu3", "gpu4", "gpu5"]:
        destination = get_available_gpus(required_gpus)
    return destination


def RoundRobin(required_gpus: int) -> Destination | None:
    with Session(db.engine) as session:
        last_server = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "last_server")
        ).one()

<<<<<<< HEAD
    destination = get_available_gpus_at(last_server.value, required_gpus)
=======
    result['server'] = last_server.value
    gpus = get_gpus()

    available_resources = [gpu for gpu in gpus if gpu.server == result['server']]

    for gpu in available_resources[:required_gpus]:
        result['gpus'].append(gpu.id)
>>>>>>> 131ffc4ddd559a59ab56f83a9e5bd76fba0b6e37

    with Session(db.engine) as session:
        last_server = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "last_server")
        ).one()
        next_server = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "next_server")
<<<<<<< HEAD
        ).one()
        # update the last server and the next server
=======
        ).first()

>>>>>>> 131ffc4ddd559a59ab56f83a9e5bd76fba0b6e37
        last_server.value = next_server.value
        if next_server.value == 'gpu3':
            next_server.value = 'gpu4'
        elif next_server.value == 'gpu4':
            next_server.value = 'gpu5'
        elif next_server.value == 'gpu5':
            next_server.value = 'gpu3'
        session.commit()

<<<<<<< HEAD
    if len(destination.gpus) < required_gpus:
        return None
    return destination
=======
    # if there are enough gpus, return the server and the gpus
    if len(available_resources) >= required_gpus:
        logging.info(f"RoundRobin: {result}")
        return result
    else:
        return None
>>>>>>> 131ffc4ddd559a59ab56f83a9e5bd76fba0b6e37
