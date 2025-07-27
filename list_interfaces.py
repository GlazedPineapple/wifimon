#!/bin/env ./.venv/bin/python3

import re
import os

def get_interfaces():
    try:
        # Use /sys/class/net to get list of network interfaces
        interfaces = os.listdir('/sys/class/net')
        return interfaces
    except Exception as e:
        return [f"Error: {str(e)}"]