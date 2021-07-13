import threading
from typing import Callable

from PyQt5.QtCore import (QObject)


class Worker(QObject):
    """
    Interface for interaction with thread class.
    """

    def __init__(self, target: Callable, *args, **kwargs):
        super().__init__()
        self._target = target
        self._args = args
        self._kwargs = kwargs
        self._thread: threading.Thread
        self._result = None

    def _call_target(self):
        self._result = self._target(*self._args, **self._kwargs)

    def run(self):
        """
        Runs worker.
        """
        self._thread = threading.Thread(target=self._call_target)
        self._thread.start()

    def is_finished(self):
        """
        Returns True if worker finish him work.
        """
        return not self._thread.is_alive()

    def get_result(self):
        """
        Returns result of target if thread is finished else None.
        """
        return self._result
