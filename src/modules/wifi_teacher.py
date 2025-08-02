#!/bin/env ./.venv/bin/python3


# Module for teaching/ Learning Mode
# learning mode for WiFi packet analysis
# This module captures and explains WiFi packets in real-time.
from scapy.all import sniff
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11ProbeReq, Dot11Deauth
from modules.module import Module
from abc import ABC, abstractmethod
import atexit

class TeacherModule(Module, ABC):
    def __init__(self, iface: str):
        super().__init__('WiFi Teacher Module')
        self.iface = iface
        if len(iface) == 0:
            exit(1)
        atexit.register(self.cleanup)

    def cleanup(self):
        if self._task_thread.is_alive():
            print('Setting stop event thread is alive')
        self._stop_event.set()


    def _task(self):
        def explain(packet):
            if packet.haslayer(Dot11Beacon):
                self.output_queue.put("[BEACON] Access Point advertising its presence.")
            elif packet.haslayer(Dot11ProbeReq):
                self.output_queue.put("[PROBE REQUEST] Device searching for known networks.")
            elif packet.haslayer(Dot11Deauth):
                self.output_queue.put("[DEAUTH] Disconnect frame – can be used for reassociation or attacks.")
            elif packet.haslayer(Dot11):
                self.output_queue.put("[802.11 FRAME] Other management or control packet.")

            self.output_queue.put(f"Captured: {packet.summary()}")

        sniff(iface=self.iface, prn=explain, store=0, stop_filter=lambda _: self._stop_event.is_set())

        print(f'{__name__}: stopped')
