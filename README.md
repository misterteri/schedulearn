# Schedulearn

Schedulearn is a lightweight distributed deep learning system, and that name is a contraction of "Scheduling Deep Learning". This project is intended to serve as my thesis project, and it's made on top of Docker, FastAPI, and Horovod.

# Setup

1. Setup a Conda environment with the following packages
```bash
conda create -n schedulearn python=3.11
conda activate schedulearn
```

2. Install the required dependencies
```bash
pip install -r requirements.txt
```

3. Install [httpie](https://httpie.io/)
```bash
brew install httpie # MacOS

sudo apt install httpie # linux
```

4. Run the API
```bash
cd api
python main.py
```

The API will be running on `http://localhost:5000`.

5. Start the web app
```bash
cd app
npm install
npm run dev
```

The web app will be running on `http://localhost:3000`, and go to that link in your browser to see the user interface.

# Usage

To create a job with the user interface, go to `localhost:3000/dashboard`. Fill in the input forms and send the request. 

To see all jobs in the system, go to `localhost:3000/jobs`.

If you want to send a request with Python, do
```python
import requests
r = requests.post(
    'http://localhost:5000/jobs', 
    json = {
        "name": "Pytorch Mnist",
        "type": "Pytorch",
        "container_image": "nathansetyawan96/horovod",
        "command": "python pytorch/pytorch_mnist.py",
        "required_gpus": 4,
    }
)
```

If you want to send a request with httpie, do
```bash
http post localhost:5000/jobs name="Pytorch Mnist" type="Pytorch" container_image="nathansetyawan96/horovod" command="python pytorch/pytorch_mnist.py" required_gpus=4
```

If the server receives your request, it should show the following message.
```bash
HTTP/1.1 201 Created
content-length: 38
content-type: application/json
date: Wed, 09 Nov 2022 15:03:41 GMT
server: uvicorn

{
    "message": "Job created successfully"
}
```

# Scheduling Algorithms

For now, the existing scheduling algorithms are FIFO and Round Robin. If you want to change the scheduling algorithm, just send a simple request like:

```bash
http PUT localhost:5000/algorithm/fifo
http PUT localhost:5000/algorithm/roundrobin
```

If the scheduling algorithm is changed successfully, it should show the following message.
```bash
HTTP/1.1 200 OK
content-length: 39
content-type: application/json
date: Wed, 09 Nov 2022 15:04:57 GMT
server: uvicorn

{
    "message": "Algorithm changed to FIFO"
}
```

To make sure if the scheduling algorithm is changed, run the following code.
```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("./api/database.db")
df = pd.read_sql_query("SELECT * FROM schedulearn", conn)
df
```

In the future, we will add more scheduling algorithms.