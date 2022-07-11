import os
import sqlite3
import uuid
import time

db_path = 'schedulearn.db'
def initialize() -> str:
    if not os.path.exists(db_path):
        connection = sqlite3.connect('schedulearn.db')
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job (
                id TEXT PRIMARY KEY NOT NULL, 
                job_name TEXT, 
                job_type TEXT, 
                container_image TEXT, 
                command TEXT, 
                started_at TIME, 
                completed_at TIME, 
                created_at TIME, 
                required_gpus INTEGER, 
                at_server TEXT references server(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS server (
                id TEXT PRIMARY KEY NOT NULL, 
                occupied_at TEXT references gpu(serial_no)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gpu (
                serial_no TEXT PRIMARY KEY NOT NULL, 
                server_id TEXT references server(id),
                job_id TEXT references job(id)
            )
        """)
        connection.commit()
        return "schedulearn.db has been created"
    return "schedulearn.db already exists"

def connect():
    connection = sqlite3.connect(db_path, check_same_thread=False)
    return connection

# insert_job function that returns a string
def insert_job(job: dict) -> str:
    connection = connect()
    cursor = connection.cursor()
    arrival = time.strftime("%Y/%m/%d %H:%M:%S")
    job_id = uuid.uuid5(uuid.NAMESPACE_DNS, job['name'] + arrival)
    cursor.execute("""
        INSERT INTO job (id, job_name, job_type, container_image, command, started_at, completed_at, created_at, required_gpus, at_server)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (str(job_id), job['name'], job['type'], job["image"], job["command"], "", "", arrival, job["required_gpus"], "gpu3"))
    connection.commit()
    return "a job has been inserted\n"

def get_jobs() -> list:
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM job")
    jobs = cursor.fetchall()
    return jobs