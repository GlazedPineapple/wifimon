#!/bin/env ./.venv/bin/python3

# probe_tracker.py
from scapy.all import sniff, Dot11, Dot11ProbeReq, Dot11Elt
import queue
from abc import ABC
from modules.module import Module

class ProbeTrackerModule(Module, ABC):
    def __init__(self, iface: str):
        super().__init__('Probe Tracker Module')
        self._iface = iface

    def _task(self):
        seen = set()

        def handler(packet):
            if packet.haslayer(Dot11ProbeReq):
                ssid = "<Hidden>"
                if packet.haslayer(Dot11Elt):
                    try:
                        ssid = packet[Dot11Elt].info.decode(errors='ignore')
                    except Exception:
                        pass
                mac = packet.addr2
                key = (ssid, mac)
                if key not in seen:
                    seen.add(key)
                    msg = f"[PROBE REQUEST] Device: {mac} | Looking for SSID: '{ssid}'"
                    try:
                        self._output_queue.put(msg, timeout=0.1)
                    except queue.Full:
                        pass

        sniff(iface=self._iface, prn=handler, store=0, stop_filter=lambda _: self._stop_event.is_set())

        print(f'{__name__}: stopped')
