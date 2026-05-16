#!/usr/bin/env python3


from http_response import HTTPResponse
from calculator import Calculator


class CalculatorHandler:
    RESOURCES = {'/op1', '/op2', '/calculate'}

    METHODS = {
        '/op1': {'GET', 'PUT'},
        '/op2': {'GET', 'PUT'},
        '/calculate': {'POST'},
    }

    OPERATIONS = {'+', '-', '*', '/'}

    def __init__(self):
        self._op1 = 0.0
        self._op2 = 0.0

    def handle(self, request):

        path = request.get_path()
        method = request.get_method()

        if path not in self.RESOURCES:
            return HTTPResponse.not_found()

        if method not in self.METHODS.get(path, set()):
            return HTTPResponse.method_not_allowed()

        if path == '/op1':
            return self._handle_op1(method, request)
        elif path == '/op2':
            return self._handle_op2(method, request)
        elif path == '/calculate':
            return self._handle_calculate(request)

        return HTTPResponse.not_found()

    def _handle_op1(self, method, request):
        if method == 'GET':
            return HTTPResponse.ok(body=Calculator.format_result(self._op1))

        elif method == 'PUT':
            try:
                op1 = request.get_body().strip()
                self._op1 = float(op1)
                return HTTPResponse.ok()
            except ValueError:
                return HTTPResponse.bad_request("неверное значение")

        return HTTPResponse.method_not_allowed()

    def _handle_op2(self, method, request):
        if method == 'GET':
            return HTTPResponse.ok(body=Calculator.format_result(self._op2))

        elif method == 'PUT':
            try:
                op2 = request.get_body().strip()
                self._op2 = float(op2)
                return HTTPResponse.ok()
            except ValueError:
                return HTTPResponse.bad_request("неверное значение")

        return HTTPResponse.method_not_allowed()

    def _handle_calculate(self, request):
        operation = request.get_header('Operation', '+')

        if operation not in self.OPERATIONS:
            return HTTPResponse.bad_request(f"неизвестная операция: {operation}")

        try:
            result = Calculator.calculate(self._op1, self._op2, operation)
            return HTTPResponse.ok(body=Calculator.format_result(result))

        except ZeroDivisionError:
            return HTTPResponse.bad_request("деление на ноль")
        except Exception as err:
            return HTTPResponse.bad_request(str(err))
