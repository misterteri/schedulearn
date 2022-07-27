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
conda create -n schedulearn python=3.10
conda activate schedulearn
```

2. Install Docker and Flask's Python SDK
```
cd api
pip install -r requirements.txt
```

3. Install httpie
```
brew install httpie # MacOS

sudo apt install httpie # linux
```

4. Run the API
```
python main.py
```

4. Sending a POST request

First, you need to open a new tab in your terminal. 

To create a new entry in the database, run:

```
http POST http://localhost:5000/api/v1/post name="tensorflow-mnist" type="TFJob" container_image="horovod/horovod:latest" command="horovodrun -np 1 -H localhost: 1 python ./tensorflow2/tensorflow2_mnist.py" no_of_gpus=1

http --json POST http://localhost:5000/jobs < test.json 
```

To fetch all the jobs in the databse, run:

```
http GET :5000/jobs
```