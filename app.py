from flask import Flask, request
import db

app = Flask(__name__)

db.initialize()

# create a POST endpoint that receives a JSON file
@app.route("/api/v1/post", methods=["POST"])
def POST():
    # parse the received JSON file
    job = request.get_json()
    msg = db.insert_job(job)
    return msg

@app.route("/api/v1/delete")
def DELETE():
    return "This is 'DELETE' endpoint"

@app.route("/api/v1/get", methods=["GET"])
def GET():
    # get all the jobs in the database from job table
    jobs = db.get_jobs()
    return str(jobs) + "\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)