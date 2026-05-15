#!/usr/bin/env python3
class FileHandler:
    @staticmethod
    def open_file(file):
        try:
            return open(file, 'r', encoding='utf-8')
        except FileNotFoundError:
            raise FileNotFoundError(f"файл {file}не найден")
        except PermissionError:
            raise PermissionError(f"нет прав на чтение файла {file}")

    @staticmethod
    def close_file(file):
        if file and not file.closed:
            try:
                file.close()
            except Exception as err:
                print(err)
                raise err


