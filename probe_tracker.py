#Probe traccker script to monitor probe requests from devices looking for WiFi networks.
# This script captures probe request frames and extracts the SSID and MAC address of the requesting device
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11ProbeReq, Dot11Elt

seen = set()

def probe_handler(packet):
    if packet.haslayer(Dot11ProbeReq):
        ssid = packet[Dot11Elt].info.decode(errors='ignore') if packet.haslayer(Dot11Elt) else "<Hidden>"
        mac = packet.addr2
        key = (ssid, mac)
        if key not in seen:
            seen.add(key)
            print(f"[PROBE REQUEST] Device: {mac} | Looking for SSID: '{ssid}'")

# Replace with your monitor-mode interface
sniff(iface="wlan0mon", prn=probe_handler, store=0)