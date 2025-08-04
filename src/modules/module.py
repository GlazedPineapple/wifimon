from __future__ import annotations

import queue
import threading
import atexit
from abc import ABC, abstractmethod


class Module(ABC):
    _running_module: Module | None = None

    def __init__(self, name: str):
        self._output_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._name = name
        self._task_thread = threading.Thread(target=self._task, name=self.name)
        atexit.register(self._cleanup)

    def start(self):
        if Module._running_module is not None:
            Module._running_module.stop()

        Module._running_module = self

        if not self._task_thread.is_alive():
            self._stop_event.clear()
            self._task_thread = threading.Thread(target=self._task, name=self.name)
            self._task_thread.start()

    def stop(self, wait_time: float | None = None):
        self._stop_event.set()
        if wait_time and self._task_thread.is_alive():
            self._task_thread.join(timeout=wait_time)

        Module._running_module = None

    def wait_for_finish(self, timeout: float = -1):
        if timeout >= 0:
            self._task_thread.join(timeout=timeout)
        else:
            self._task_thread.join()
        Module._running_module = None


    def is_running(self):
        return self._task_thread.is_alive()

    @property
    def name(self):
        return self._name

    @property
    def output_queue(self):
        return self._output_queue

    @abstractmethod
    def _task(self):
        pass

    def _cleanup(self):
        self.stop(wait_time=3)
        if Module._running_module is not None:
            Module._running_module.stop(wait_time=3)

    def __str__(self):
        return self._name
