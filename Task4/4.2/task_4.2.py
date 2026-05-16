#!/usr/bin/env python3


import subprocess
import sys

from processes import Processes
from signal_handler import SignalHandler
from parser import Parser
from command_line_processes import CommandLineProcesses
from json_formatter import JSONFormatter


def main():
    processes = Processes()
    signal_handler = SignalHandler(processes)
    parser = Parser()
    pipeline_builder = CommandLineProcesses(processes)
    formatter = JSONFormatter()

    try:
        signal_handler.set_signal_handler()

        commands, file = parser.parse_args(sys.argv[1:])

        results, last_output = pipeline_builder.run(commands, file)

        formatter.print_json(results)

        return 0

    except ValueError as err:
        print(f"<команда> [аргументы] ['<'] <файл>")
        return 1

    except FileNotFoundError as err:
        print("не найден файл")
        return 2

    except PermissionError as err:
        print("ошибка доступа")
        return 3

    except subprocess.TimeoutExpired:
        print("превышено время ожидания")
        return 4

    except Exception as err:
        print(err)
        return 5

    finally:
        signal_handler.restore_handler()


if __name__ == "__main__":
    sys.exit(main())