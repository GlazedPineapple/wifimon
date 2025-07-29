from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Elt
from scapy.layers.eap import EAPOL

def analyze_security(packet_queue, iface="wlan1"):
    def handler(pkt):
        if pkt.haslayer(EAPOL):
            src = pkt[Dot11].addr2
            dst = pkt[Dot11].addr1
            info = f"[EAPOL] Handshake detected | From: {src} To: {dst}"
            print(info)
            packet_queue.put(info)

        elif pkt.haslayer(Dot11Beacon):
            ssid = pkt[Dot11Elt].info.decode(errors='ignore')
            bssid = pkt[Dot11].addr3
            crypto = []

            cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}")
            if re.search("privacy", cap.lower()):
                crypto.append("WEP/WPA/WPA2")

            elt = pkt[Dot11Elt]
            while isinstance(elt, Dot11Elt):
                if elt.ID == 48:
                    crypto.append("WPA2")
                elif elt.ID == 221 and elt.info.startswith(b'\x00\x50\xf2\x01'):
                    crypto.append("WPA")
                elt = elt.payload.getlayer(Dot11Elt)

            info = f"[SECURITY] SSID: {ssid} | BSSID: {bssid} | Crypto: {', '.join(set(crypto)) or 'Open'}"
            print(info)
            packet_queue.put(info)

    sniff(iface=iface, prn=handler, store=0)