#!/usr/bin/env python3
import signal
import sys


class SignalHandler:
    def __init__(self, processes):
        self.processes = processes
        self.signal_handler = None

    def set_signal_handler(self):
        self.signal_handler = signal.signal(signal.SIGUSR1, self.handler)

    def handler(self):
        self.processes.finish_all()
        sys.exit(0)

    def restore_handler(self):
        if self.processes:
            signal.signal(signal.SIGUSR1, self.signal_handler)


