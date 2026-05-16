#!/usr/bin/env python3
import signal
import sys


class SignalHandler:
    def __init__(self, processes):
        self._processes = processes
        self._processes_handler = None
        self._has_signal = False

    def set_signal_handler(self):
        self._processes_handler = signal.signal(signal.SIGUSR1, self._handler)

    def _handler(self, sig, frame):
        self._has_signal = True
        self._processes.finish_all()

    def restore_handler(self):
        if self._processes_handler is not None:
            signal.signal(signal.SIGUSR1, self._handler)

    def get_signal_received(self):
        return self._has_signal
