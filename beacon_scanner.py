# Scan for nearby WiFi access points by capturing beacon frames.
#test
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt

networks = set()

def beacon_handler(packet):
    if packet.haslayer(Dot11Beacon):
        ssid = packet[Dot11Elt].info.decode(errors='ignore')
        bssid = packet[Dot11].addr3
        channel = None
        rssi = packet.dBm_AntSignal if hasattr(packet, 'dBm_AntSignal') else "N/A"

        # Find channel number in Dot11Elt layers
        elt = packet[Dot11Elt]
        while isinstance(elt, Dot11Elt):
            if elt.ID == 3:  # Channel ID
                channel = ord(elt.info) if isinstance(elt.info, bytes) else elt.info
                break
            elt = elt.payload.getlayer(Dot11Elt)

        network_id = f"{ssid} - {bssid}"
        if network_id not in networks:
            networks.add(network_id)
            print(f"[BEACON] SSID: {ssid} | BSSID: {bssid} | Channel: {channel} | RSSI: {rssi} dBm")

# Replace with the Monitor mode interface -Raspberry Pi - wlan0mon
sniff(iface="wlan0mon", prn=beacon_handler, store=0)
