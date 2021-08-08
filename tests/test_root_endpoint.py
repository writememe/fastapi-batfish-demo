"""
This test file tests all endpoints located under the URL:

http://<api_server_ip>:<api_server_port>/
"""
# Import modules
from fastapi.testclient import TestClient
import sys
import os

# Get path of the current dir under which the file is executed.
dirname = os.path.dirname(__file__)
# Append sys path so that local relative imports can work.
sys.path.append(os.path.join(dirname, ".."))

# Import main FastAPI application
from app.main import app  # noqa

# Import variables for testing
from app.shared.utilities import (
    API_ROOT_MESSAGE,
)  # noqa

# Initialise test client
client = TestClient(app)

# Global testing variables to avoid repetition


def test_root_endpoint():
    """
    Test the root API endpoint
    """
    resp = client.get("/")
    print(resp.url)
    assert resp.status_code == 200
    assert resp.json()["message"] == API_ROOT_MESSAGE
