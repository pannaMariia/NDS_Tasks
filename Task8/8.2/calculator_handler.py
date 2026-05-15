#!/usr/bin/env python3


from http_request import HTTPRequest
from http_response import HTTPResponse
from calculator import Calculator


class CalculatorHandler:

    RESOURCES = {'/op1', '/op2', '/calculate'}

    ALLOWED_METHODS = {
        '/op1': {'GET', 'PUT'},
        '/op2': {'GET', 'PUT'},
        '/calculate': {'POST'},
    }

    def __init__(self):
        self._op1 = 0.0
        self._op2 = 0.0

    def handle(self, request: HTTPRequest) -> HTTPResponse:

        path = request.get_path()
        method = request.get_method()

        # Проверка существования ресурса
        if path not in self.RESOURCES:
            return HTTPResponse.not_found()

        # Проверка поддержки метода для данного ресурса
        if method not in self.ALLOWED_METHODS.get(path, set()):
            return HTTPResponse.method_not_allowed()

        # Маршрутизация
        if path == '/op1':
            return self._handle_op1(method, request)
        elif path == '/op2':
            return self._handle_op2(method, request)
        elif path == '/calculate':
            return self._handle_calculate(request)

        return HTTPResponse.not_found()

    def _handle_op1(self, method: str, request: HTTPRequest) -> HTTPResponse:
        if method == 'GET':
            return HTTPResponse.ok(body=Calculator.format_result(self._op1))

        elif method == 'PUT':
            try:
                value = request.get_body().strip()
                self._op1 = float(value)
                return HTTPResponse.ok()
            except ValueError:
                return HTTPResponse.bad_request("Invalid number")

        return HTTPResponse.method_not_allowed()

    def _handle_op2(self, method: str, request: HTTPRequest) -> HTTPResponse:
        if method == 'GET':
            return HTTPResponse.ok(body=Calculator.format_result(self._op2))

        elif method == 'PUT':
            try:
                value = request.get_body().strip()
                self._op2 = float(value)
                return HTTPResponse.ok()
            except ValueError:
                return HTTPResponse.bad_request("Invalid number")

        return HTTPResponse.method_not_allowed()

    def _handle_calculate(self, request: HTTPRequest) -> HTTPResponse:
        # Получаем операцию из заголовка (по умолчанию '+')
        operation = request.get_header('Operation', '+')

        # Проверка поддерживаемой операции
        if operation not in Calculator.OPERATIONS:
            return HTTPResponse.bad_request(f"Unsupported operation: {operation}")

        try:
            result = Calculator.calculate(self._op1, self._op2, operation)
            result_str = Calculator.format_result(result)
            return HTTPResponse.ok(body=result_str)

        except ZeroDivisionError:
            return HTTPResponse.bad_request("Division by zero")
        except Exception as e:
            return HTTPResponse.bad_request(str(e))