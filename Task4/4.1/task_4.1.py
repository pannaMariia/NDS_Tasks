#!/usr/bin/env python3
import subprocess
import sys
from processes import Processes
from signal_handler import SignalHandler
from parser import Parser
from process_runner import ProcessRunner
from json_formatter import JSONFormatter




def main():

    processes = Processes()
    signal_handler = SignalHandler(processes)
    argument_parser = Parser()
    process_runner = ProcessRunner(processes)
    formatter = JSONFormatter()

    process = None
    file = None

    try:
        signal_handler.set_signal_handler()

        command, file = argument_parser.parse_args(sys.argv[1:])
        process = process_runner.run(command, file)

        stdout_data, returncode = ProcessRunner.communicate_process(process)
        result = formatter.format(command[0], returncode, stdout_data)
        formatter.print_json([result])

        return 0

    except ValueError as e:
        print(f"[ERROR] Ошибка в аргументах: {e}", file=sys.stderr)
        print(f"Использование: {sys.argv[0]} <команда> [аргументы] ['<'] <файл>", file=sys.stderr)
        return 1

    except FileNotFoundError as e:
        print("не найден файл")
        return 2

    except PermissionError as e:
        print("ошибка доступа")
        return 3

    except subprocess.TimeoutExpired:
        print("превышено время ожидания")
        return 4

    except Exception as err:
        print(err)
        return 5

    finally:
        if process:
            processes.remove(process)

        signal_handler.restore_handler()


if __name__ == "__main__":
    sys.exit(main())

