import logging
import database as db
from lib import get_gpus
from sqlmodel import Session, select, col

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

def RoundRobin(required_gpus: int) -> dict | None:
    result = {"server": "", "gpus": []}
    with Session(db.engine) as session:
        last_server = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "last_server")
        ).first()

    result['server'] = last_server.value
    gpus = get_gpus()

    available_resources = [gpu for gpu in gpus if gpu.server == result['server']]

    for gpu in available_resources[:required_gpus]:
        result['gpus'].append(gpu.id)

    with Session(db.engine) as session:
        last_server = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "last_server")
        ).first()
        next_server = session.exec(
            select(db.Schedulearn)
            .where(col(db.Schedulearn.configuration) == "next_server")
        ).first()

        last_server.value = next_server.value
        if next_server.value == 'gpu3':
            next_server.value = 'gpu4'
        elif next_server.value == 'gpu4':
            next_server.value = 'gpu5'
        elif next_server.value == 'gpu5':
            next_server.value = 'gpu3'
        session.commit()

    # if there are enough gpus, return the server and the gpus
    if len(available_resources) >= required_gpus:
        logging.info(f"RoundRobin: {result}")
        return result
    else:
        return None