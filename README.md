[![fastapi-batfish-demo](https://github.com/writememe/fastapi-batfish-demo/actions/workflows/main.yaml/badge.svg)](https://github.com/writememe/fastapi-batfish-demo/actions/workflows/main.yaml)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

# FastAPI x Batfish Demo

This repository contains a FastAPI implementation to present Batfish
pandas dataframe data to an end user.

## Supported Environments

This application is only supported on:
 - Python 3.7 or greater
 - Linux/unix machines only


 ## Installation/Operating Instructions

Below is the method to run the `fastapi-batfish-demo` using Python 3.x.

### Python 3.X

The most popular way of running this application is using it in a standard Python environment. To do so, please follow the options below:

1) Clone the repository to the machine on which you will run the application from:

```git
git clone https://github.com/writememe/fastapi-batfish-demo.git
cd fastapi-batfish-dem
```

2) Create the virtual environment to run the application in:

```console
virtualenv --python=`which python3` venv
source venv/bin/activate
```
4) Install the requirements for `fastapi-batfish-demo`
```
pip install -r requirements.txt
```

5) (Optional)Set environmental variable, which is used by the application as location of the Batfish "database" files:

```bash
export BATFISH_DB="<github_repo_directory>/db/"
```
6) Validate these environmental variables by entering the following command:

```
env | grep BATFISH_DB
```
You should see the two environment variables set.

7) Start the FastAPI application, whereby the `--port` argument is the TCP port you want to listen on:

```python3
uvicorn app.main:app --port 8004 --reload
```

8) Open up your web-browser and navigate to the following URL, substituting the server address for whatever
is specific to your environment:

http://<your_server_ip>:<your_port>/docs

For example:  

http://127.0.0.1:8004/docs



