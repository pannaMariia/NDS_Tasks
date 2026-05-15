#!/usr/bin/env python3
import sys

from http_server import HTTPServer
from calculator_handler import CalculatorHandler


def main():
    handler = CalculatorHandler()

    server = HTTPServer(host='0.0.0.0', port=10000)
    server.set_handler(handler.handle)
    server.start()

    return 0


if __name__ == "__main__":
    sys.exit(main())