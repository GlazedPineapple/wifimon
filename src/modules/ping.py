#!/bin/env ./.venv/bin/python3
from abc import ABC
from modules.module import Module
from ping3 import ping


class PingModule(Module, ABC):

    def __init__(self, host: str, count: int = 10):
        super().__init__('Ping Module')
        self._host: str = host
        self._count: int = count

    def _task(self):
        for i in range(self._count):
            if self._stop_event.is_set():
                return

            result = ping(self._host, timeout=2)
            if result is None:
                self._output_queue.put(f"Request {i + 1}: Timed out")
            else:
                self._output_queue.put(f"Request {i + 1}: {round(result * 1000, 2)} ms")

        print(f'{__name__}: stopped')