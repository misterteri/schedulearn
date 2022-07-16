# %%
from sqlmodel import select, Session, create_engine
from database import Server, Gpu
# connect to the database
engine = create_engine("sqlite:///schedulearn.sqlite3", echo=True)

# get all the servers in the database
with Session(engine) as session:
    statement = select(Server)
    results = session.execute(statement)
    for server in results:
        print(server)

# %%
with Session(engine) as session:
    statement = select(Gpu)
    results = session.execute(statement)
    for gpu in results:
        print(gpu)