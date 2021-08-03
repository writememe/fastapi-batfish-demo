"""
This module contains all the "backend" functions
which are used to perform backend tasks such as:
- Retrieve data from databases
- Transform backend data for frontend usage
"""
# Import modules
from typing import Union, Dict
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
    file_dir: str = BATFISH_DATABASE,
) -> str:
    """
    Get the correct filename based on the CSV naming standard
    from the "Batfish Database".

    Args:
        TODO

    Returns:
        TODO

    Raises:
        TODO
    """
    bf_csv_file_name = f"{file_prefix}-{date_stamp}-{file_suffix}.csv"
    return bf_csv_file_name


def convert_bf_csv_file_to_bf(
    csv_file_path: str, index_method: Union[str, int] = 0
) -> pd.DataFrame:
    """
    Read the Batfish CSV data file and convert it to a pandas dataframe for further usage.

    Args:
        csv_file_path:
        index_method:

    Returns:
        df: A pandas dataframe for further processing.

    Raises:
        N/A
    """
    df = pd.read_csv(
        csv_file_path,
        index_col=index_method,
    )
    return df


def convert_df_to_json(
    df: pd.DataFrame, orient: str = "index", indent: int = 2
) -> Dict:
    raw_result = df.to_json(orient=orient, indent=indent)
    print(f"Type: {type(raw_result)}")
    dict_result = json.loads(raw_result)
    return dict_result


def filter_interfaces_by_node(
    df: pd.DataFrame, node: str, exact_match: bool = True
) -> pd.DataFrame:
    """
    Args:
        df:
        node:
        exact_match:

    Returns:
        df: A pandas dataframe for further processing.

    Raises:
        N/A
    """
    if exact_match:
        df = df[df["Node"] == node]
    else:
        df = df[df["Node"].str.contains(node)]
    return df


def filter_interfaces_by_active(
    df: pd.DataFrame, node: str = None, active: bool = True
) -> pd.DataFrame:
    """
    Args:
        df:
        node:
        exact_match:

    Returns:
        df: A pandas dataframe for further processing.

    Raises:
        N/A
    """
    if node:
        df = df[(df["Interface"].str.startswith(node)) & (df["Active"] == active)]
    else:
        df = df[df["Active"] == active]
    return df


def get_all_interfaces_active(
    date_stamp: str = "2021-08-03",
    file_prefix: str = "dfjt",
    file_suffix: str = "interfaceProperties",
    file_dir: str = BATFISH_DATABASE,
    node: str = None,
    active: bool = True,
):
    bf_csv_file = get_bf_csv_file_name(
        date_stamp=date_stamp,
        file_prefix=file_prefix,
        file_suffix=file_suffix,
        file_dir=file_dir,
    )
    bf_csv_file_path = os.path.join(file_dir, bf_csv_file)
    if os.path.exists(bf_csv_file_path):
        df = convert_bf_csv_file_to_bf(csv_file_path=bf_csv_file_path, index_method=0)
        interface_df = filter_interfaces_by_active(df=df, node=node, active=active)
        print(interface_df)
        print("*********")
        interface_dict = convert_df_to_json(df=interface_df, orient="index")
        print(interface_dict)
        return interface_dict
    else:
        interface_dict = None
        return interface_dict


if __name__ == "__main__":
    get_all_interfaces_active()
