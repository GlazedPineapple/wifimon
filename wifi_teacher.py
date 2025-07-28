#!/bin/env ./.venv/bin/python3


#Module for teaching/ Learning Mode
#learning mode for WiFi packet analysis
#This module captures and explains WiFi packets in real-time.
from scapy.all import sniff
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11ProbeReq, Dot11Deauth

def explain(packet):
    if packet.haslayer(Dot11Beacon):
        print("[BEACON] Access Point advertising its presence.")
    elif packet.haslayer(Dot11ProbeReq):
        print("[PROBE REQUEST] Device searching for known networks.")
    elif packet.haslayer(Dot11Deauth):
        print("[DEAUTH] Disconnect frame – can be used for reassociation or attacks.")
    elif packet.haslayer(Dot11):
        print("[802.11 FRAME] Other management or control packet.")
   
    print(f"Captured: {packet.summary()}")

# Replace with your monitor interface, e.g., 'wlan0mon'
sniff(iface="wlan0mon", prn=explain, store=0)

