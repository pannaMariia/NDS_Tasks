#!/usr/bin/env python3
import json
import signal


class JSONFormatter:
    @staticmethod
    def format(command, returncode, output):
        result = {
            "name": command,
            "code": returncode
        }

        if returncode < 0:
            signal_code = -returncode
            try:
                signal_name = signal.Signals(signal_code).name
            except ValueError:
                signal_name = "Terminated"

            result["signal"] = signal_name
            if output:

                result["output"] = output
            else:
                result["output"] = ""
        else:
            if output and output.strip():
                result["output"] = output.rstrip('\n')

        return result

    @staticmethod
    def print_json(results):
        print(json.dumps(results, ensure_ascii=False, indent=4))