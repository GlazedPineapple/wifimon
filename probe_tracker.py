#!/bin/env ./.venv/bin/python3

# probe_tracker.py
from scapy.all import sniff, Dot11, Dot11ProbeReq, Dot11Elt
import queue

def probe_track(iface: str, output_q: queue.Queue, stop_flag):
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
                    output_q.put(msg, timeout=0.1)
                except queue.Full:
                    pass

    sniff(iface=iface, prn=handler, store=0, stop_filter=lambda _: stop_flag.stop)
