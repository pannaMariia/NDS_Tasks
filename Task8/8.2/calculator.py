#!/usr/bin/env python3

class Calculator:

    @staticmethod
    def calculate(op1, op2, operation):

        if operation == '+':
            return op1 + op2
        elif operation == '-':
            return op1 - op2
        elif operation == '*':
            return op1 * op2
        elif operation == '/':
            if op2 == 0:
                raise ZeroDivisionError("деление на ноль запрещено")
            return op1 / op2
        else:
            raise ValueError(f"неизвестная операция: {operation}")

    @staticmethod
    def format_result(result):
        if isinstance(result, float) and result.is_integer():
            return str(int(result))
        return str(result)
