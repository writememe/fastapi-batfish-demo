"""
This is a basic toolkit to interact with the Batfish
Server. It performs the following operations:

- Initialises new snapshots
- Load existing snapshots
- Retrieves some Batfish answers to dataframes
- Saves those dataframes to CSV files.
"""

# Import modules
import pandas as pd
import os
from pybatfish.client.commands import (
    bf_session,
    bf_init_snapshot,
    bf_set_network,
    bf_set_snapshot,
    bf_list_snapshots,
)
from pybatfish.question.question import load_questions, list_questions
from pybatfish.question import bfq
import time
import pathlib

# Get path of the current dir under which the file is executed.
dirname = os.path.dirname(__file__)

"""
The following block is the set of global variables used throughout
the toolkit. Adjust these as needed.
"""
# Generate a timestamp based on today's date
CURRENT_DATESTAMP = time.strftime("%Y-%m-%d")
# Specify a network name for the Batfish snapshot
NETWORK_NAME = "DFJT-LAB-NETWORK"
# Format a snapshot name, based on todays date
SNAPSHOT_NAME = f"{NETWORK_NAME}-{CURRENT_DATESTAMP}"
# Join together where this file is run and the sample_configs/
# directory
SNAPSHOT_BASE_DIR = os.path.join(dirname, "..", "sample_configs")
# Specify the snapshot directory to be used
SNAPSHOT_DIR = "example_network"
# Join altogether so we can access the right folder containing the configs
SNAPSHOT_PATH = os.path.join(SNAPSHOT_BASE_DIR, SNAPSHOT_DIR)
# Set the Batfish Service IP, hardcoded by default
BATFISH_SERVICE_IP = "10.0.0.54"  # Your specified Batfish IP Address
# Specify the output directory for the results to be saved to.
OUTPUT_DIR = os.path.join(dirname, "..", "db")
# Create output directory and/or check that it exists
pathlib.Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def init_snapshot(
    BATFISH_SERVICE_IP: str, NETWORK_NAME: str, SNAPSHOT_NAME: str, SNAPSHOT_PATH: str
) -> None:
    """
    Initialise a Batfish snapshot, so that we can perform an analysis of the bundled configurations.

    Args:
        BATFISH_SERVICE_IP: The IP address which is hosting the Batfish Docker instance.
        NETWORK_NAME: The name of the network which like would like to refer to the snapshot as.
        SNAPSHOT_NAME: The name of the snapshot.
        SNAPSHOT_PATH: The path where all the configurations are, which will are
        used to initialise the configuration from.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Setup session
    bf_session.host = BATFISH_SERVICE_IP
    # Set network
    bf_set_network(NETWORK_NAME)
    # Initialise snapshot
    bf_init_snapshot(SNAPSHOT_PATH, name=SNAPSHOT_NAME, overwrite=True)
    # Load questions
    load_questions()
    # List questions
    list_questions()


def load_snapshot(BATFISH_SERVICE_IP: str, NETWORK_NAME: str, SNAPSHOT_NAME: str):
    """
    Load an existing batfish snapshot, so that analysis can be performed.

    Args:
        BATFISH_SERVICE_IP: The IP address which is hosting the Batfish Docker instance.
        NETWORK_NAME: The name of the network which like would like to refer to the snapshot as.
        SNAPSHOT_NAME: The name of the snapshot.

    Returns:
        N/A

    Raises:
        N/A
    """
    # Setup session
    bf_session.host = BATFISH_SERVICE_IP
    # Set network
    bf_set_network(NETWORK_NAME)
    # List snapshots
    bf_list_snapshots()
    # Load the snapshot which we are after.
    bf_set_snapshot(SNAPSHOT_NAME)
    # Load questions
    load_questions()
    # List questions
    list_questions()


def get_all_interface_properties() -> pd.DataFrame:
    """
    Get all possible interface properties on all nodes.

    Args:
        N/A

    Returns:
        df: A pandas Dataframe containing all interface properties
        discovered in the snapshot.

    Raises:
        N/A
    """
    # Query batfish for all interface properties
    df = bfq.interfaceProperties().answer().frame()
    # Assign a name to the Dataframe for usage in other functions
    df.name = "interfaceProperties"
    return df


def batfish_df_to_csv(df: pd.DataFrame, output_dir: str, base_filename: str) -> str:
    """
    Take a batfish pandas Dataframe and save it to a CSV file

    Args:
        df: The batfish pandas Dataframe to be written to file.
        output_dir: The output directory to save the CSV file to.
        base_filename: The base filename, which will be appended to as needed
        when generating and saving the CSV file.

    Returns:
        csv_formatted_name: The CSV formatted name for usage in further operations.


    Raises:
        N/A
    """
    # Format the output file name together, so we can identify which
    # Dataframe is stored in which output CSV
    # Example Name: dfjt-2021-08-02-interfaceProperties.csv
    csv_formatted_filename = f"{base_filename}-{df.name}.csv"
    csv_file_path = os.path.join(output_dir, csv_formatted_filename)
    print(f"Saving dataframe to '{csv_file_path}'")
    df.to_csv(csv_file_path)
    return csv_formatted_filename


def prepare_snapshots(
    BATFISH_SERVICE_IP: str,
    NETWORK_NAME: str,
    SNAPSHOT_NAME: str,
    SNAPSHOT_PATH: str,
    create_snapshot: bool = True,
) -> None:
    """
    This function toggles either the creation of a new snapshot, or load an existing one.

    Args:
        BATFISH_SERVICE_IP: The IP address which is hosting the Batfish Docker instance.
        NETWORK_NAME: The name of the network which like would like to refer to the snapshot as.
        SNAPSHOT_NAME: The name of the snapshot.
        SNAPSHOT_PATH: The path where all the configurations are, which will are
        used to initialise the configuration from.
        create_snapshot: Boolean to indicate whether to create a snapshot, or load an existing one.

    Returns:
        N/A

    Raises:
        N/A
    """
    # If/else block to either load an existing snapshot or initialise a new one.
    if create_snapshot:
        # Initialise new batfish snapshot
        init_snapshot(BATFISH_SERVICE_IP, NETWORK_NAME, SNAPSHOT_NAME, SNAPSHOT_PATH)
    else:
        # Load existing snapshot
        load_snapshot(BATFISH_SERVICE_IP, NETWORK_NAME, SNAPSHOT_NAME)


def main():
    prepare_snapshots(
        BATFISH_SERVICE_IP,
        NETWORK_NAME,
        SNAPSHOT_NAME,
        SNAPSHOT_PATH,
        create_snapshot=True,
    )
    # Retrieve all interface properties into a Dataframe
    interface_df = get_all_interface_properties()
    # Format the base CSV filename, to use in the naming standard
    # of files
    base_csv_filename = f"dfjt-{CURRENT_DATESTAMP}"
    # Save the data to CSV and return the filename
    interface_csv_filename = batfish_df_to_csv(
        df=interface_df, output_dir=OUTPUT_DIR, base_filename=base_csv_filename
    )
    print(f"Results saved at: {os.path.join(OUTPUT_DIR, interface_csv_filename)}")
    pass


if __name__ == "__main__":
    main()
