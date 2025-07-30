from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Elt
from scapy.layers.eap import EAPOL
from modules.module import Module
from abc import ABC


class SecurityAnalyzerModule(Module, ABC):
    def __init__(self, iface: str):
        super().__init__('Security Analyzer Module')
        self._iface = iface

    def _task(self):
        def handler(pkt):
            if pkt.haslayer(EAPOL):
                src = pkt[Dot11].addr2
                dst = pkt[Dot11].addr1
                info = f"[EAPOL] Handshake detected | From: {src} To: {dst}"
                print(info)
                self._output_queue.put(info)

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
                self._output_queue.put(info)

        sniff(iface=self._iface, prn=handler, store=0, stop_filter=lambda _: self._stop_event.is_set())
