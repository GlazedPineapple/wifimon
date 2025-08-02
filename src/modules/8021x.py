#!/bin/env ./.venv/bin/python3
import subprocess
import queue
from abc import ABC
from modules.module import Module
import signal

#/home/aokovacs/Documents/wifimon/eaphammer/ --bssid 1C:7E:E5:97:79:B1  --essid Example  --channel 2  --interface wlan1  --auth wpa-eap  --creds



class mod_8021x(Module, ABC):
    def __init__(self, iface: str, essid: str):
        self.iface=iface
        if len(iface) == 0:
            exit(1)
        self.essid=essid
        

    def _task(self):
        process = subprocess.Popen(["/bin/env", "sudo", "/home/aokovacs/Documents/wifimon/eaphammer_manager.sh", self.iface, self.essid])
        self._stop_event.wait()
        process.send_signal(signal.SIGINT)
        print(f'{__name__}: stopped')
