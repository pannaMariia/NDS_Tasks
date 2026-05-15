#!/usr/bin/env python3
from typing import Dict, Optional


class HTTPResponse:
    STATUS_MESSAGES = {
        200: "OK",
        400: "Bad Request",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
    }

    def __init__(self):
        self.status_code = 200
        self.headers: Dict[str, str] = {}
        self.body = ""
        self._set_default_headers()

    def _set_default_headers(self):
        self.headers["Connection"] = "close"

    def set_status(self, code):
        self.status_code = code

    def set_content_type(self, content_type):
        self.headers["Content-Type"] = content_type

    def set_body(self, body):
        self.body = body
        self.headers["Content-Length"] = str(len(body.encode('utf-8')))

    def set_header(self, name, value):
        self.headers[name] = value

    def to_bytes(self):
        status_message = self.STATUS_MESSAGES.get(self.status_code, "Unknown")

        # Первая строка
        response = f"HTTP/1.1 {self.status_code} {status_message}\r\n"

        # Заголовки
        for key, value in self.headers.items():
            response += f"{key}: {value}\r\n"

        response += "\r\n"
        response += self.body

        return response.encode('utf-8')

    @classmethod
    def ok(cls, body: str = "", content_type: str = "text/plain"):
        resp = cls()
        resp.set_status(200)
        resp.set_content_type(content_type)
        resp.set_body(body)
        return resp

    @classmethod
    def not_found(cls):
        resp = cls()
        resp.set_status(404)
        resp.set_content_type("text/plain")
        resp.set_body("404 Not Found")
        return resp

    @classmethod
    def method_not_allowed(cls):
        resp = cls()
        resp.set_status(405)
        resp.set_content_type("text/plain")
        resp.set_body("")
        return resp

    @classmethod
    def bad_request(cls, message: str = "Bad Request"):
        resp = cls()
        resp.set_status(400)
        resp.set_content_type("text/plain")
        resp.set_body(message)
        return resp

    @classmethod
    def internal_error(cls):
        resp = cls()
        resp.set_status(500)
        resp.set_content_type("text/plain")
        resp.set_body("Internal Server Error")
        return resp