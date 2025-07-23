#analyzes encryption types of Wi-Fi networks using packet capture 
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt

def get_encryption(packet):
    if not packet.haslayer(Dot11Beacon):
        return None

    enc_type = "Open"
    capability = packet.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}").split('+')

    if "privacy" in capability:
        enc_type = "WEP"
        elt = packet.getlayer(Dot11Elt)
        while elt:
            if elt.ID == 48:
                enc_type = "WPA2"
                break
            elif elt.ID == 221 and elt.info.startswith(b'\x00P\xf2\x01\x01\x00'):
                enc_type = "WPA"
                break
            elt = elt.payload.getlayer(Dot11Elt)

    return enc_type

def handle_packet(packet):
    if packet.haslayer(Dot11Beacon):
        ssid = packet[Dot11Elt].info.decode(errors='ignore')
        bssid = packet[Dot11].addr3
        encryption = get_encryption(packet)
        if encryption:
            print(f"[+] SSID: {ssid} | BSSID: {bssid} | Security: {encryption}")

# Replace with your monitor interface, e.g., 'wlan0mon'
sniff(iface="wlan0mon", prn=handle_packet, timeout=30)
