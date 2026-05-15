#!/usr/bin/env python3

from typing import Dict, Tuple


class HTTPRequest:

    def __init__(self, raw_data: str):
        self.method = ""
        self.path = ""
        self.headers: Dict[str, str] = {}
        self.body = ""
        self._parse(raw_data)

    def _parse(self, raw_data: str):
        lines = raw_data.split('\r\n')

        if not lines:
            return

        # Парсим первую строку (Request-Line)
        first_line = lines[0].split(' ')
        if len(first_line) >= 2:
            self.method = first_line[0].upper()
            self.path = first_line[1]

        # Парсим заголовки и тело
        headers_parsed = False
        body_lines = []

        for i, line in enumerate(lines[1:], 1):
            # Пустая строка означает конец заголовков
            if line == "" and not headers_parsed:
                headers_parsed = True
                continue

            if not headers_parsed:
                # Парсим заголовок
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    self.headers[key] = value
            else:
                # Собираем тело запроса
                body_lines.append(line)

        self.body = '\r\n'.join(body_lines)

    def get_header(self, name, default):
        return self.headers.get(name, default)

    def get_body(self):
        return self.body

    def get_path(self):
        return self.path

    def get_method(self):
        return self.method

    def __repr__(self):
        return f"HTTPRequest(method={self.method}, path={self.path})"