"""
This module contains all the "backend" functions
which are used to perform backend tasks such as:
- Retrieve data from databases
- Transform backend data for frontend usage
"""
# Import modules
from typing import Union, Dict, Optional
import os
import pandas as pd
import json
import sys

# Get path of the current dir under which the file is executed.
dirname = os.path.dirname(__file__)
# Append sys path so that local relative imports can work.
sys.path.append(os.path.join(dirname, "..", ".."))
# Local endpoint imports
from app.shared.utilities import BATFISH_DATABASE  # noqa (import not at top)


def get_bf_csv_file_name(
    date_stamp: str = "2021-08-03",
    file_prefix: str = "dfjt",
    file_suffix: str = "interfaceProperties",
) -> str:
    """
    Get the correct filename based on the CSV naming standard
    from the "Batfish Database".

    Args:
        date_stamp: A formatted date stamp indicating the day of the file to be retrieved.
            Example: 2021-08-03 - August 3rd 2021.
        file_prefix: The prefix of the file naming standard, prior to the date stamp.
        file_suffix: The suffix of the file naming standard, after the date stamp.
    Returns:
        bf_csv_file_name: The formatted CSV file name, based on the arguments
        passing into the function.

    Raises:
        N/A
    """
    # Formatted the file name, for example dfjt-2021-08-03-interfaceProperties.csv
    bf_csv_file_name = f"{file_prefix}-{date_stamp}-{file_suffix}.csv"
    return bf_csv_file_name


def convert_bf_csv_file_to_df(
    csv_file_path: str, index_method: Union[str, int] = 0
) -> pd.DataFrame:
    """
    Read the Batfish CSV data file and convert it to a pandas dataframe for further usage.

    Args:
        csv_file_path: The fully qualified path to the Batfish CSV file which should be
        converted to a Pandas dataframe.
        index_method: The indexing method to use for the dataframe.
            Doco: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html

    Returns:
        df: A pandas dataframe for further processing.

    Raises:
        N/A
    """
    # Read CSV and convert into a Pandas dataframe
    df = pd.read_csv(
        csv_file_path,
        index_col=index_method,
    )
    return df


def convert_df_to_json(
    df: pd.DataFrame, orient: str = "index", indent: int = 2
) -> Dict:
    """
    Convert a Pandas dataframe to JSON and prepare for presentation
    to the frontend API endpoint by converting to a dictionary.
    Args:
        df: The pandas dataframe to be converted.
        orient: The orientation method when converting to JSON.
            Doco: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_json.html # noqa
        indent: The number of indentation(s) for the JSON data
        structure.

    Returns:
        dict_result: A dictionary representation of the original Pandas
        dataframe

    Raises:
        N/A
    """
    # Convert Pandas dataframe to JSON
    raw_result = df.to_json(orient=orient, indent=indent)
    # Convert to dictionary, for further usage
    dict_result = json.loads(raw_result)
    return dict_result


def filter_interfaces_by_active(
    df: pd.DataFrame, node: Optional[str] = None, active: bool = True
) -> pd.DataFrame:
    """
    Filter all interface properties by a particular node, and
    perform a match for active or inactive interfaces, based
    on the `active` boolean flag.

    Args:
        df: A pandas dataframe for filtering.
        node: The name of the node on which the dataframe should be
        filtered, if supplied.
        active: Boolean to specify whether active or inactive interfaces
        are filtered.

    Returns:
        df: A pandas dataframe for further processing.

    Raises:
        N/A
    """
    # If a node is supplied, filter on the node AND the Active column
    if node:
        df = df[(df["Interface"].str.startswith(node)) & (df["Active"] == active)]
    # Else, filter on the Active column only
    else:
        df = df[df["Active"] == active]
    return df


# Functions which interface with the Frontend API functions.


def get_all_interfaces_active(
    date_stamp: str = "2021-08-03",
    file_prefix: str = "dfjt",
    file_suffix: str = "interfaceProperties",
    file_dir: str = BATFISH_DATABASE,
    node: Optional[str] = None,
    active: bool = True,
) -> Dict:
    """
    Locate and load data in a datestamped Batfish CSV file, filter based on node (if supplied)
    and active boolean flag and return dictionary back to API response.

    Args:
        date_stamp: A formatted date stamp indicating the day of the file to be retrieved.
            Example: 2021-08-03 - August 3rd 2021.
        file_prefix: The prefix of the file naming standard, prior to the date stamp.
        file_suffix: The suffix of the file naming standard, after the date stamp.
        file_dir: The directory which contains the 'Batfish database' of CSV files.
        node: The node name (if supplied) to filter Pandas dataframes on.
        active: A boolean to indicate whether active or inactive interfaces should be
        returned in the filter.

    Returns:
        interface_dict:
            If successful, a dictionary containing the Pandas dataframe results.
            If unsuccessful, None is returned for further processing.

    Raises:
        N/A
    """
    # Generate the correctly formatted CSV file name
    bf_csv_file = get_bf_csv_file_name(
        date_stamp=date_stamp,
        file_prefix=file_prefix,
        file_suffix=file_suffix,
    )
    # Join with Batfish directory and assign to variable
    bf_csv_file_path = os.path.join(file_dir, bf_csv_file)
    # If the file is present,
    if os.path.exists(bf_csv_file_path):
        # Convert the CSV file to a dataframe
        df = convert_bf_csv_file_to_df(csv_file_path=bf_csv_file_path, index_method=0)
        # Perform the appropriate filtering on the dataframe.
        interface_df = filter_interfaces_by_active(df=df, node=node, active=active)
        # Convert dataframe to dictionary
        interface_dict = convert_df_to_json(df=interface_df, orient="index")
        # Return dictionary.
        return interface_dict
    # Else, if the file isn't present
    else:
        # Return None for interface dict, so that value can be processed outside
        # this function
        interface_dict = None
        return interface_dict
