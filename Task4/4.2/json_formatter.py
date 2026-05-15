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
            signal_num = -returncode

            # SIGUSR1 macOS = 30
            # Linux = 10
            if signal_num in (10, 30):
                signal_name = "Terminated"
            else:
                try:
                    signal_name = signal.Signals(signal_num).name
                except ValueError:
                    signal_name = f"Signal {signal_num}"

            result["signal"] = signal_name
            result["output"] = output if output else ""
        else:
            if output and output.strip():
                result["output"] = output.rstrip('\n')

        return result

    @staticmethod
    def print_json(results):
        print(json.dumps(results, ensure_ascii=False, indent=4))