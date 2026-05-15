#!/usr/bin/env python3
class Processes:
    def __init__(self):
        self.processes = []

    def add(self, process):
        self.processes.append(process)

    def remove(self, process):
        if process in self.processes:
            self.processes.remove(process)

    def finish_all(self):
        for process in self.processes:
            if process.poll() is None:
                process.terminate()

