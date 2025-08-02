#!/bin/env ./.venv/bin/python3
import subprocess
import queue
from abc import ABC
from modules.module import Module

#/home/aokovacs/Documents/wifimon/eaphammer/ --bssid 1C:7E:E5:97:79:B1  --essid Example  --channel 2  --interface wlan1  --auth wpa-eap  --creds



class mod_8021x(Module, ABC):
    def __init__(self, iface: str, essid: str):
        self.iface=iface
        self.essid=essid

    def _task(self):
        process = subprocess.Popen(["/bin/env", "sudo", f"/home/aokovacs/Documents/wifimon/eaphammer/ --bssid 1C:7E:E5:97:79:B1  --essid {self.essid}  --channel 2  --interface {self.iface}  --auth wpa-eap  --creds"])
        self._stop_event.wait()
        process.communicate(input=b"\r\n")
        print(f'{__name__}: stopped')
