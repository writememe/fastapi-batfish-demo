"""
This module contains shared utilies over multiple
parts of the codebase, to prevention repetition
"""
# Import modules
import os

# Get path of the current dir under which the file is executed.
dirname = os.path.dirname(__file__)

# Define 404 errors returned from different API endpoint
DEFAULT_404_RESPONSE = {"error": "Endpoint not found"}
API_ENDPOINT_404_RESPONSE = "Item not found"
# Attempt to use the environmental variable BATFISH_DB and if not set,
# use the default for this project
try:
    BATFISH_DATABASE = os.environ["BATFISH_DB"]
except KeyError as key_err:
    print(
        f"WARNING: Environmental Variable 'BATFISH_DB' not set. {key_err}"
        "Setting to default value."
    )
    BATFISH_DATABASE = os.path.join(dirname, "..", "db")
# Define an example dataframe response for usage in API endpoint documentation
EXAMPLE_INTERFACE_DF = {
    "df_data": {
        "27": {
            "Interface": "lab-csr-01[GigabitEthernet2]",
            "Access_VLAN": 0,
            "Active": False,
            "All_Prefixes": "[]",
            "Allowed_VLANs": 0,
            "Auto_State_VLAN": True,
            "Bandwidth": 1000000000,
            "Blacklisted": False,
            "Channel_Group": 0,
            "Channel_Group_Members": "[]",
            "DHCP_Relay_Addresses": "[]",
            "Declared_Names": "['GigabitEthernet2']",
            "Description": "interface description",
            "Encapsulation_VLAN": 0,
            "HSRP_Groups": "[]",
            "HSRP_Version": 0,
            "Incoming_Filter_Name": 0,
            "MLAG_ID": 0,
            "MTU": 1500,
            "Native_VLAN": 0,
            "Outgoing_Filter_Name": "some filter name",
            "PBR_Policy_Name": "some policies",
            "Primary_Address": "some IP addreses",
            "Primary_Network": "some networks",
            "Proxy_ARP": True,
            "Rip_Enabled": False,
            "Rip_Passive": False,
            "Spanning_Tree_Portfast": False,
            "Speed": 1000000000,
            "Switchport": False,
            "Switchport_Mode": "NONE",
            "Switchport_Trunk_Encapsulation": "DOT1Q",
            "VRF": "default",
            "VRRP_Groups": "[]",
            "Zone_Name": "some zones",
        }
    }
}

DEFAULT_422_RESPONSE = {
    "detail": [
        {
            "loc": ["query", "active"],
            "msg": "value could not be parsed to a boolean",
            "type": "type_error.bool",
        }
    ]
}
