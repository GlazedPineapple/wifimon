#!/bin/env ./.venv/bin/python3

import os
from modules.module import Module
from abc import ABC


class ListInterfacesModule(Module, ABC):
    def __init__(self):
        super().__init__('List Interfaces Module')

    def _task(self):
        try:
            interfaces = os.listdir('/sys/class/net')
            iface_str = 'Available interfaces: '
            for iface in interfaces:
                iface_str += str(iface) + ' '
            print(f'Putting "{iface_str}"')
            self.output_queue.put(iface_str)
        except Exception as e:
            return [f"Error: {str(e)}"]

        print(f'{__name__}: stopped')

