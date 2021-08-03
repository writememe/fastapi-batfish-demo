"""
This module contains shared utilies over multiple
parts of the codebase, to prevention repetition
"""
# Import modules
import os

DEFAULT_404_RESPONSE = {"error": "Endpoint not found"}
BATFISH_DATABASE = os.environ["BATFISH_DB"]
API_ENDPOINT_404_RESPONSE = "Item not found"
