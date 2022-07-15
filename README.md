# Schedulearn

Schedulearn is contraction of "Scheduling Deep Learning", and the goal of this project is just exactly like the name.
This project is intended to serve as my thesis project, and it's made on top of several tools:

1. Docker
2. Flask
3. Horovod

## Setup

1. Setup a Conda environment with the following packages

```
conda env create -n schedulearn python=3.10
conda activate schedulearn
```

2. Install Docker and Flask's Python SDK
```
pip install --user docker flask
```

3. Run the API
```
FLASK_APP=app.py FLASK_ENV=development flask run
```

4. Sending a POST request

First, you need to open a new tab in your terminal. In your new tab, run:
```
curl -X POST -H "Content-Type: application/json" -d @./test.json http://localhost:5000/api/v1/post
```

# Progress

- [x] Create a database called `schedulearn.db`
    - [x] Create `job` table
        - [x] Populate job table
    - [x] Create `gpu` table
        - [x] Populate `gpu` table
    - [x] Create `server` table
        - [x] Populate `server` table
- [x] Create a REST API with Flask
    - [ ] `/post` endpoint
        - [x] Receive a JSON file with training model requirements
            - [x] has `jobname`
            - [x] has `jobtype`
            - [x] has `image`
            - [x] has `command`
            - [x] has `requiredgpus`
        - [x] Store the info in JSON to the `Job` table in database
        - [ ] Validate the JSON file with JSON Schema
    - [ ]  `/delete` endpoint
        - [ ] if a model is on progress, delete the pod immediately, as well as the metadata of a model in the database
        - [ ] If a training model is completed, delete the model info in the database
    - [ ] `/get` endpoint
        - [x] Get all running jobs
        - [ ] Get all in-queue
        - [ ] Get all completed jobs
- [ ]  Create a scheduler
    - [ ] Find jobs that have `started_at` and `completed_at` empty and schedule it
    - [ ] Algorithmically weigh a training model
    - [ ] Algorithmically assign a model to a certain server
        - [x] Kuhn-Munkres algorithm ([source](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linear_sum_assignment.html))
        - [ ] Genetic algorithm
        - [ ] Branch and Bound algorithm
    - [ ] Algorithmically allocate a number of GPUs to a traninig model
        - [ ] Use [AFS-L](https://www.usenix.org/conference/nsdi21/presentation/hwang) algorithm
        - [ ] Elastic FIFO
        - [ ] Elastic SRFJ
        - [ ] Elastic Tiresias
        - [ ] FFDL Optimizer
        - [ ] FIFO
        - [ ] SRFJ
        - [ ] Tiresias
    - [ ] Keep track of a model's number of migrations