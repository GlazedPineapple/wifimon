#!/bin/env ./.venv/bin/python3

from scapy.all import sniff
from scapy.packet import Packet
from scapy.all import IP

src_ip = '192.168.4.2'
dst_ip = '192.168.4.1'


def handle_packet(pkt: Packet):
    # print(pkt)
    pkt.show()
    if src_ip in pkt:
        ip_layer = pkt[src_ip]
        if True:  #ip_layer.dst == dst_ip:
            print(f"[+] Intercepted packet: {ip_layer.src} -> {ip_layer.dst}")


sniff(iface="wlan0", filter="ip", prn=handle_packet, store=0)
