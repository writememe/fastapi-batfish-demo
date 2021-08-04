"""
This module contains all the Batfish data
related API endpoints
"""
# Import modules
from fastapi import APIRouter, HTTPException
import os
import sys

# Get path of the current dir under which the file is executed.
dirname = os.path.dirname(__file__)
# Append sys path so that local relative imports can work.
sys.path.append(os.path.join(dirname, "..", "..", "..", ".."))
# Local endpoint imports
from app.shared.utilities import (
    BATFISH_DATABASE,
    API_ENDPOINT_404_RESPONSE,
    EXAMPLE_INTERFACE_DF,
)  # noqa (import not at top)
from app.backend.toolkit import get_all_interfaces_active  # noqa (import not at top)

# Instantiate an instance of APIRouter
router = APIRouter()


# Frontend API endpoint functions
@router.get(
    "/interfaces/",
    summary="Retrieve active or interface Batfish interfaces",
    response_description="Eligible batfish dataframes in JSON format.",
    responses={
        200: {
            "description": "The eligible Pandas dataframe(s) nested inside the `df_data` key.",
            "content": {"application/json": {"example": EXAMPLE_INTERFACE_DF}},
        }
    },
)
async def retrieve_all_interfaces_active(
    date_stamp: str = "2021-08-03",
    file_prefix: str = "dfjt",
    file_suffix: str = "interfaceProperties",
    node: str = None,
    active: bool = True,
):
    # Retrieve all applicable interfaces based on the parameters
    # supplied in the API endpoint
    interface_dict = get_all_interfaces_active(
        date_stamp=date_stamp,
        file_prefix=file_prefix,
        file_suffix=file_suffix,
        file_dir=BATFISH_DATABASE,
        node=node,
        active=active,
    )
    # If data is found, return back to API endpoint for serving
    if interface_dict:
        return {"df_data": interface_dict}
    # Else, return 404 indicating that data was not found
    else:
        raise HTTPException(status_code=404, detail=API_ENDPOINT_404_RESPONSE)
