#!/usr/bin/env python3

from typing import Dict


class HTTPRequest:

    def __init__(self, raw_data: str):
        self.method = ""
        self.path = ""
        self.headers: Dict[str, str] = {}
        self.body = ""
        self._parse(raw_data)

    def _parse(self, request):
        request_parts = request.split('\r\n')

        if not request_parts:
            return

        first_part = request_parts[0].split(' ')
        if len(first_part) >= 2:
            self.method = first_part[0].upper()
            self.path = first_part[1]

        headers_parsed = False
        body = []

        for i, part in enumerate(request_parts[1:], 1):
            if part == "" and not headers_parsed:
                headers_parsed = True
                continue

            if not headers_parsed:
                if ': ' in part:
                    key, value = part.split(': ', 1)
                    self.headers[key] = value
            else:
                body.append(part)

        self.body = '\r\n'.join(body)

    def get_header(self, name, default):
        return self.headers.get(name, default)

    def get_body(self):
        return self.body

    def get_path(self):
        return self.path

    def get_method(self):
        return self.method
