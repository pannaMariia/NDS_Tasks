#!/usr/bin/env python3
import subprocess


class CommandLineProcesses:

    def __init__(self, processes):
        self._processes = processes

    def run(self, commands, stdin_file=None):

        cl_processes = []
        pre_stdout = None

        stdin = None
        if stdin_file:
            try:
                stdin = open(stdin_file, 'r', encoding='utf-8')
            except Exception as err:
                raise FileNotFoundError(f"не удается открыть файл {stdin_file}: {err}")

        try:
            for i, command in enumerate(commands):
                flag_last = (i == len(commands) - 1)

                if i == 0 and stdin:
                    stdin_source = stdin
                else:
                    stdin_source = pre_stdout

                process = subprocess.Popen(
                    command,
                    stdin=stdin_source,
                    stdout=subprocess.PIPE if not flag_last else subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True
                )

                cl_processes.append(process)
                self._processes.add(process)

                if not flag_last:
                    pre_stdout = process.stdout

            results = []
            last_output = None

            for i, process in enumerate(cl_processes):
                command = commands[i]
                is_last = (i == len(cl_processes) - 1)

                if is_last:
                    stdout, _ = process.communicate()
                    if stdout:
                        last_output = stdout.rstrip('\n')
                else:
                    process.wait()

                result = {
                    "name": command[0],
                    "code": process.returncode
                }

                if is_last and last_output and last_output.strip():
                    result["output"] = last_output

                if process.returncode < 0:
                    signal_num = -process.returncode
                    if signal_num in (10, 30):
                        result["signal"] = "Terminated"
                    else:
                        result["signal"] = f"Signal {signal_num}"
                    result["output"] = ""

                results.append(result)

            return results, last_output

        finally:
            if stdin:
                stdin.close()