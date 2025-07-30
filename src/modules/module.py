import queue
import threading
import atexit
from abc import ABC, abstractmethod


class Module(ABC):
    def __init__(self, name: str):
        self._output_queue = queue.Queue()
        self._stop_event = threading.Event()
        self._name = name
        self._task_thread = threading.Thread(target=self._task, name=self.name)
        atexit.register(self._cleanup)

    def start(self):
        if not self._task_thread.is_alive():
            self._stop_event.clear()
            self._task_thread = threading.Thread(target=self._task, name=self.name)
            self._task_thread.start()

    def stop(self, wait: bool = False):
        self._stop_event.set()
        if wait and self._task_thread.is_alive():
            self._task_thread.join(timeout=3)

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
        self.stop(wait=True)

    def __str__(self):
        return self._name
