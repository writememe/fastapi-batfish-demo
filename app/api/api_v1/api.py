"""
This module contains the APIRouter which
is used to import one or more endpoint modules
"""
# Import modules
from fastapi import APIRouter
import os
import sys

# Get path of the current dir under which the file is executed.
dirname = os.path.dirname(__file__)
# Append sys path so that local relative imports can work.
sys.path.append(os.path.join(dirname, "..", "..", ".."))

# Local endpoint imports
from app.api.api_v1.endpoints import batfish  # noqa (top level import)
from app.shared.utilities import DEFAULT_404_RESPONSE  # noqa (top level import)

# Instance APIRouter instance
router = APIRouter()
# Import the batfish router, and assign default tags, prefixes
# and responses
router.include_router(
    batfish.router,
    prefix="/bf",
    tags=["batfish"],
    responses={404: DEFAULT_404_RESPONSE},
)
