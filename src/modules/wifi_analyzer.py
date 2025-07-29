#!/bin/env ./.venv/bin/python3

from scapy.all import sniff, Dot11, Dot11Beacon, Dot11ProbeReq, Dot11Elt
import queue

def wifi_analyze(iface: str, output_q: queue.Queue, stop_flag):
    seen_beacons = set()
    seen_probes = set()

    def handler(packet):
        # Beacon Frames
        if packet.haslayer(Dot11Beacon):
            ssid = packet[Dot11Elt].info.decode(errors='ignore') if packet.haslayer(Dot11Elt) else "<Hidden>"
            bssid = packet[Dot11].addr3
            key = f"BEACON {bssid}-{ssid}"
            if key not in seen_beacons:
                seen_beacons.add(key)
                msg = f"[BEACON] SSID: {ssid} | BSSID: {bssid}"
                try:
                    output_q.put(msg, timeout=0.1)
                except queue.Full:
                    pass

        # Probe Requests
        elif packet.haslayer(Dot11ProbeReq):
            ssid = packet[Dot11Elt].info.decode(errors='ignore') if packet.haslayer(Dot11Elt) else "<Hidden>"
            mac = packet.addr2
            key = f"PROBE {mac}-{ssid}"
            if key not in seen_probes:
                seen_probes.add(key)
                msg = f"[PROBE] Device: {mac} | Looking for SSID: '{ssid}'"
                try:
                    output_q.put(msg, timeout=0.1)
                except queue.Full:
                    pass

    sniff(iface=iface, prn=handler, store=0, stop_filter=lambda _: stop_flag.stop)