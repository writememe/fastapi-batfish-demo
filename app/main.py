"""
FastAPI main application module
"""
# Import modules
from fastapi import FastAPI
import os

# Local FastAPI module imports
from app.api.api_v1.api import router as api_router
from app.shared.utilities import API_ROOT_MESSAGE, API_TITLE, API_SEMANTIC_VER

# Get path of the current dir under which the file is executed.
dirname = os.path.dirname(__file__)

# Define tag metadata to be attributed to certain endpoints
tag_metadata = [
    {
        "name": "batfish",
        "description": "Batfish related endpoints which retrieve and serve Batfish data",
    }
]
# Instantiate FastAPI Class
app = FastAPI(
    openapi_tags=tag_metadata,
    description="A demonstration of building an API server to retrieve and serve Batfish data.",
    version=API_TITLE,
    title=API_SEMANTIC_VER,
)
# Import router into FastAPI
app.include_router(api_router, prefix="/api/v1")


# An indicative root endpoint
@app.get("/")
async def root_api_server():
    return {"message": API_ROOT_MESSAGE}
