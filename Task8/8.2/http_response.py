#!/usr/bin/env python3


class HTTPResponse:
    MESSAGES = {
        200: "OK",
        400: "Bad Request",
        404: "Not Found",
        405: "Method Not Allowed",
        500: "Internal Server Error",
    }

    def __init__(self):
        self.status_code = 200
        self.status_message = "OK"
        self.headers = {"Connection": "close"}
        self.body = ""

    def set_status(self, code):
        self.status_code = code

    def set_content_type(self, content_type):
        self.headers["Content-Type"] = content_type

    def set_body(self, body):
        self.body = body
        self.headers["Content-Length"] = str(len(body.encode('utf-8')))

    def set_header(self, head, status):
        self.headers[head] = status

    def to_bytes_str(self):
        message = self.MESSAGES.get(self.status_code, "Unknown")

        response = f"HTTP/1.1 {self.status_code} {message}\r\n"
        for key, value in self.headers.items():
            response += f"{key}: {value}\r\n"
        response += "\r\n"
        response += self.body

        return response.encode('utf-8')

    @classmethod
    def ok(cls, body: str = ""):
        response = cls()
        response.set_status(200)
        response.set_content_type("text/plain")
        response.set_body(body)
        return response

    @classmethod
    def not_found(cls):
        response = cls()
        response.set_status(404)
        response.set_content_type("text/plain")
        response.set_body("404 Not Found")
        return response

    @classmethod
    def method_not_allowed(cls):
        response = cls()
        response.set_status(405)
        response.set_content_type("text/plain")
        response.set_body("")
        return response

    @classmethod
    def bad_request(cls, message:str = "Bad Request"):
        response = cls()
        response.set_status(400)
        response.set_content_type("text/plain")
        response.set_body(message)
        return response

    @classmethod
    def internal_error(cls):
        response = cls()
        response.set_status(500)
        response.set_content_type("text/plain")
        response.set_body("Internal Server Error")
        return response
