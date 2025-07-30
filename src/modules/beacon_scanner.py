#!/bin/env ./.venv/bin/python3
from scapy.all import sniff, Dot11, Dot11Beacon, Dot11Elt
from modules.module import Module
from abc import ABC
import queue


class BeaconScannerModule(Module, ABC):
    def __init__(self, iface: str):
        super().__init__('Beacon Scanner Module')
        self._iface = iface

    def _task(self):
        print(f'{__name__}: Scanner starting on "{self._iface}"')
        seen = set()

        def handler(pkt):
            if pkt.haslayer(Dot11Beacon):
                ssid = pkt[Dot11Elt].info.decode(errors='ignore')
                bssid = pkt[Dot11].addr3
                rssi = pkt.dBm_AntSignal if hasattr(pkt, 'dBm_AntSignal') else "N/A"
                channel = None

                elt = pkt[Dot11Elt]
                while isinstance(elt, Dot11Elt):
                    if elt.ID == 3:
                        channel = elt.info[0] if isinstance(elt.info, bytes) else elt.info
                        break
                    elt = elt.payload.getlayer(Dot11Elt)

                net_id = f"{ssid} - {bssid}"
                if net_id not in seen:
                    seen.add(net_id)
                    message = f"[BEACON] SSID: {ssid} | BSSID: {bssid} | Channel: {channel} | RSSI: {rssi} dBm"
                    try:
                        self._output_queue.put(message, timeout=0.1)
                    except queue.Full:
                        pass

        sniff(iface=self._iface, prn=handler, store=0, stop_filter=lambda _: self._stop_event.is_set())

        print(f'{__name__}: stopped')
