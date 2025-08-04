#!/bin/env ./.venv/bin/python3
import subprocess
import queue
import time
from abc import ABC
from modules.module import Module
# from module import Module
import signal
import os
import atexit
import threading
import typing

# /home/aokovacs/Documents/wifimon/eaphammer/ --bssid 1C:7E:E5:97:79:B1  --essid Example  --channel 2  --interface wlan1  --auth wpa-eap  --creds

# Find eaphammer_manager.sh
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
EAP_MANAGER_PATH = f'{PROJECT_ROOT}/eaphammer_manager.sh'
if not os.path.isfile(EAP_MANAGER_PATH):
    raise FileNotFoundError(f'{__name__}: Could not find eaphammer_manager.sh script')


class mod_8021x(Module, ABC):
    def __init__(self, iface: str, target_essid: str, target_bssid: str | None = None):
        super().__init__('8021x Module')

        self._iface = iface
        if len(iface) == 0:
            raise ValueError(f'{__name__}: Invalid interface argument')

        self._essid = target_essid
        self._bssid = '1C:7E:E5:97:79:B1' if target_bssid is None else target_bssid
        self._process: subprocess.Popen[str] | None = None

        atexit.register(self.cleanup)

    def _task(self):
        self._process = subprocess.Popen(["/bin/env", "sudo", EAP_MANAGER_PATH, self._iface, self._essid],
                                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True,)

        if self._process.stdout is None:
            raise ValueError("stdout was none")

        def stdout_thread(stdout: typing.IO[str], output_queue: queue.Queue):
            try:
                while True:
                    output_queue.put(stdout.readline())
            except:
                pass

        thread = threading.Thread(target=stdout_thread, args=(self._process.stdout, self._output_queue))
        thread.start()

        self._stop_event.wait()
        print(f'{__name__}: killing process')
        self._process.send_signal(signal.SIGINT)
        (stdout, stderr) = self._process.communicate()
        print(f'{__name__}: stdout: {stdout}\nstderr: {stderr}')
        self._output_queue.put(stdout)
        self._output_queue.put(stderr)
        print(f'{__name__}: Process returned ({self._process.returncode})')
        print(f'{__name__}: stopped')

    def stop(self, wait_time: float | None = None):
        print(f'{__name__}: stopping')
        super().stop(wait_time)
        if self._process is not None:
            self._process.send_signal(signal.SIGTERM)

    def cleanup(self):
        if self._process is not None:
            self._process.send_signal(signal.SIGTERM)
