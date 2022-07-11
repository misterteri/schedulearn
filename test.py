# %%
# connect to schedulearn.db
import sqlite3

connection = sqlite3.connect('schedulearn.db')
cursor = connection.cursor()

# check if job table has any data
cursor.execute("SELECT * FROM job")
jobs = cursor.fetchall()
print(jobs)