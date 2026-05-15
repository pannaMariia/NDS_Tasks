#!/usr/bin/env python3
class Parser:
    @staticmethod
    def parse_args(args):
        if len(args) < 1:
            raise ValueError("не указана команда для запуска")

        if '<' in args:
            sep_indx = args.index('<')

            if sep_indx == 0:
                raise ValueError("не указана команда")

            if sep_indx + 1 >= len(args):
                raise ValueError("не указано имя файла")



            file = args[sep_indx + 1]
            command = args[:sep_indx]

            return command, file
        else:
            return args, None

