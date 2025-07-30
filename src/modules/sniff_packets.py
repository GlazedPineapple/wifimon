#!/bin/env ./.venv/bin/python3

from scapy.all import sniff
from abc import ABC
from modules.module import Module


class PacketSnifferModule(Module, ABC):
    def __init__(self, iface: str):
        super().__init__('Packet Sniffer Module')
        self._iface = iface

    def _task(self):
        def packet_handler(packet):
            summary = packet.summary()
            self._output_queue.put(summary)

        sniff(iface=self._iface, prn=packet_handler, store=0, stop_filter=lambda _: self._stop_event.is_set())

        print(f'{__name__}: stopped')
