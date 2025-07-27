#!/bin/env ./.venv/bin/python3
def start(int):
    """
    #TODO:
    This function is a placeholder for DHCP-related functionality.
    Currently, it does not perform any operations.
    """
    print("DHCP start function called")
    return {
        "Started dhcp server on intLAN"
    }    
def stop():
    """
     #TODO:
    This function is a placeholder for DHCP-related functionality.
    Currently, it does not perform any operations.
    """
    print("DHCP stop function called")
  

def leases() -> dict[str, str]:
    """
     #TODO:
    This function is a placeholder for DHCP-related functionality.
    Currently, it does not perform any operations.
    """
    print("DHCP leases function called")
    return {
        "00:00:00:00:00": "100.100.100.100",
        "11:11:11:11:11": "101.101.101.101"
    }


def client(int):
    #obtains dhcp ip on given int
     #TODO:
    ip = "10.0.3.31"
    return ip


