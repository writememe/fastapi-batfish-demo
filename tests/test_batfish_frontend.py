"""
This test file tests all endpoints located under the URL:

http://<api_server_ip>:<api_server_port>/api/v1/bf/
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
    DEFAULT_422_RESPONSE,
    API_ENDPOINT_404_RESPONSE,
)  # noqa

# Initialise test client
client = TestClient(app)

# Global testing variables to avoid repetition
GOOD_DATESTAMP = "2021-08-03"
GOOD_FILE_PREFIX = "dfjt"
GOOD_FILE_SUFFIX = "interfaceProperties"
GOOD_NODE = "lab-csr-01"
BAD_DATESTAMP = "3021-08-03"
BAD_NODE = "bad-lab-csr-01"
BAD_FILE_PREFIX = "bad-dfjt"
BAD_FILE_SUFFIX = "badinterfaceProperties"
API_VERSION = "v1"
API_PREFIX = f"api/{API_VERSION}/bf"
GOOD_TEST_BATFISH_DIR = os.path.join(dirname, "test_db")
BAD_TEST_BATFISH_DIR = os.path.join(dirname, "bad_test_db")
JSON_MIME_TYPE = "application/json"
ENDPOINT_404_DICT = {"detail": API_ENDPOINT_404_RESPONSE}


def test_retrieve_all_interfaces_active_good():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with all good arguments.
    """
    resp = client.get(
        f"{API_PREFIX}/interfaces/?date_stamp={GOOD_DATESTAMP}&file_prefix={GOOD_FILE_PREFIX}"
        f"&file_suffix={GOOD_FILE_SUFFIX}&active=true&node={GOOD_NODE}"
    )
    assert resp.status_code == 200
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert len(resp.json()["df_data"]) > 0


def test_retrieve_all_interfaces_active_good_timestamp():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with a good datestamp.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?date_stamp={GOOD_DATESTAMP}")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert len(resp.json()["df_data"]) > 0


def test_retrieve_all_interfaces_active_bad_timestamp():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with a bad datestamp.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?date_stamp={BAD_DATESTAMP}")
    assert resp.status_code == 404
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert resp.json() == ENDPOINT_404_DICT


def test_retrieve_all_interfaces_active_good_file_prefix():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with a good file prefix.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?file_prefix={GOOD_FILE_PREFIX}")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert len(resp.json()["df_data"]) > 0


def test_retrieve_all_interfaces_active_bad_file_prefix():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with a bad file prefix.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?file_prefix={BAD_FILE_PREFIX}")
    assert resp.status_code == 404
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert resp.json() == ENDPOINT_404_DICT


def test_retrieve_all_interfaces_active_good_file_suffix():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with a good file suffix.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?file_suffix={GOOD_FILE_SUFFIX}")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert len(resp.json()["df_data"]) > 0


def test_retrieve_all_interfaces_active_bad_file_suffix():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with a bad file suffix.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?file_suffix={BAD_FILE_SUFFIX}")
    assert resp.status_code == 404
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert resp.json() == ENDPOINT_404_DICT


def test_retrieve_all_interfaces_active_good_node():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with a good node.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?node={GOOD_NODE}")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert len(resp.json()["df_data"]) > 0


def test_retrieve_all_interfaces_active_bad_node():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with a bad node.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?file_suffix={BAD_NODE}")
    assert resp.status_code == 404
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert resp.json() == ENDPOINT_404_DICT


def test_retrieve_all_interfaces_active_good_active_true():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with the active boolean set to true.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?active=true")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert len(resp.json()["df_data"]) > 0


def test_retrieve_all_interfaces_active_good_active_false():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with the active boolean set to false.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?active=false")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert len(resp.json()["df_data"]) > 0


def test_retrieve_all_interfaces_active_good_active_bad():
    """
    Test the `/api/v1/bf/interfaces/` endpoint with the active boolean set to a
    non-boolean value.
    """
    resp = client.get(f"{API_PREFIX}/interfaces/?active=bad")
    assert resp.status_code == 422
    assert resp.headers["content-type"] == JSON_MIME_TYPE
    assert resp.json() == DEFAULT_422_RESPONSE
