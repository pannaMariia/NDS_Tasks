#!/usr/bin/env python3
import subprocess
from file_handler import FileHandler
class ProcessRunner:
    def __init__(self, processes):
        self._processes = processes

    def run(self, command, file=None):

        file_handler = None

        try:
            if file:
                file_handler = FileHandler.open_file(file)

            process = subprocess.Popen(
                command,
                stdin = file_handler,
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT,
                text = True
            )

            self._processes.add(process)

            return process

        except Exception as err:
            FileHandler.close_file(file_handler)
            raise err

    @staticmethod
    def communicate_process(process):
        try:
            stdout_data, _ = process.communicate()
            return stdout_data or "", process.returncode
        except Exception as err:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    process.kill()
            raise err