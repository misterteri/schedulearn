from flask import Flask
app = Flask(__name__)

@app.route("/api/v1/post")
def POST():
    return "This is 'POST' endpoint"

@app.route("/api/v1/delete")
def DELETE():
    return "This is 'DELETE' endpoint"

@app.route("/api/v1/put")
def PUT():
    return "This is 'PUT' endpoint"