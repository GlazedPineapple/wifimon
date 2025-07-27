#!/bin/env ./.venv/bin/python3

import os

def monitorMode(iface: str, mode: bool):
    try:
        if mode == 1:
            os.system("ifconfig " + iface + " down")
            os.system("iwconfig " + iface + " mode monitor")
            os.system("ifconfig " + iface + " up")
        elif mode == 0:
            os.system("ifconfig " + iface + " down")
            os.system("iwconfig " + iface + " mode Managed")
            os.system("ifconfig " + iface + " up")
       
    except:
        print("Exception: {e}")

