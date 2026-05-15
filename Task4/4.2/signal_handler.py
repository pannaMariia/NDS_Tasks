#!/usr/bin/env python3
import signal
import sys


class SignalHandler:
    def __init__(self, processes):
        self._processes = processes
        self._original_handler = None

    def set_signal_handler(self):
        self._original_handler = signal.signal(signal.SIGUSR1, self._handler)

    def _handler(self, sig, frame):
        self._processes.finish_all()
        sys.exit(0)

    def restore_handler(self):
        if self._original_handler is not None:
            signal.signal(signal.SIGUSR1, self._original_handler)
