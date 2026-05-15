#!/usr/bin/env python3

class Parser:
    @staticmethod
    def parse_args(args):
        if len(args) < 1:
            raise ValueError("не указана команда для запуска")

        file = None
        new_args = []
        i = 0
        while i < len(args):
            if args[i] == '<':
                if i + 1 >= len(args):
                    raise ValueError("не указан файл")
                if file is not None:
                    raise ValueError("можно указать только одно перенаправление '<'")
                file = args[i + 1]
                i += 2
            else:
                new_args.append(args[i])
                i += 1

        if '|' not in new_args:
            return [new_args], file

        commands = []
        cur_command = []

        for arg in new_args:
            if arg == '|':
                if not cur_command:
                    raise ValueError("пустая команда")
                commands.append(cur_command)
                cur_command = []
            else:
                cur_command.append(arg)

        if not cur_command:
            raise ValueError("последняя команда не указана")
        commands.append(cur_command)

        if len(commands) < 2:
            raise ValueError("нужно минимум 2 команды")

        return commands, file