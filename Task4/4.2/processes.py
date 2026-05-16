#!/usr/bin/env python3
import signal


class Processes:
    def __init__(self):
        self._processes = []

    def add(self, process):
        self._processes.append(process)

    def remove(self, process):
        if process in self._processes:
            self._processes.remove(process)

    def finish_all(self):
        for process in self._processes:
            if process.poll() is None:
                process.send_signal(signal.SIGUSR1)

