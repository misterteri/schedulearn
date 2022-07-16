# Schedulearn

Schedulearn is contraction of "Scheduling Deep Learning", and the goal of this project is just exactly like the name.
This project is intended to serve as my thesis project, and it's made on top of several tools:

1. Docker
2. FastAPI
3. Pydantic
4. SQLModel
5. Horovod

## Setup

1. Setup a Conda environment with the following packages

```
conda env create -n schedulearn python=3.10
conda activate schedulearn
```

2. Install Docker and Flask's Python SDK
```
pip install docker fastapi "uvicorn[standard]"
```

3. Run the API
```
uvicorn main:app --reload --port 5000
```

4. Sending a POST request

First, you need to open a new tab in your terminal. In your new tab, run:
```
http POST http://localhost:5000/api/v1/post name="tensorflow-mnist" type="TFJob" image="horovod/horovod:latest" command="horovodrun -np 1 -H localhost: 1 python ./tensorflow2/tensorflow2_mnist.py" required_gpus=1
```

# Progress

- [x] Create a database called `schedulearn.db`
    - [x] Create tables using SQLModel to prevent SQL injection
        - [x] Create `job` table
            - [x] Populate job table
        - [x] Create `gpu` table
            - [x] Populate `gpu` table
        - [x] Create `server` table
            - [x] Populate `server` table
- [x] Create a REST API with FastAPI
    - [x] `/post` endpoint
        - [x] Receive a JSON file with training model requirements
            - [x] has `jobname`
            - [x] has `jobtype`
            - [x] has `image`
            - [x] has `command`
            - [x] has `requiredgpus`
        - [x] Store the info in JSON to the `Job` table in database
        - [x] Validate the received JSON files with Pydantic
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