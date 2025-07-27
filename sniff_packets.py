#!/bin/env ./.venv/bin/python3

from scapy.all import sniff, Dot11
import queue

def sniff_packets(iface: str, packet_queue: queue.Queue, stop_flag):
    print('sniff_packets')
    def packet_handler(packet):
        summary = packet.summary()
        packet_queue.put(summary)

    print('sniff')
    sniff(iface=iface, prn=packet_handler, store=0, stop_filter=lambda p: stop_flag.stop)
