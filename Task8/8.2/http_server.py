#!/usr/bin/env python3

import socket

from http_request import HTTPRequest
from http_response import HTTPResponse


class HTTPServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 10000):
        self.host = host
        self.port = port
        self._server_socket = None
        self._running = False
        self._handler = None

    def set_handler(self, handler):
        self._handler = handler

    def start(self):
        try:
            self._create_server_socket()
            self._running = True

            print("сервер запущен")

            while self._running:
                try:
                    client_socket, client_address = self._server_socket.accept()
                    print(f"подклюдчен клиент: {client_address}")
                    self._handle_client(client_socket)
                except OSError:
                    break

        except KeyboardInterrupt:
            print(f"cервер остановлен пользователем")
        except Exception as err:
            print(err)
        finally:
            self._stop()

    def _create_server_socket(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(5)

    def _handle_client(self, client_socket):
        try:
            data = self._get_request(client_socket)
            if not data:
                return

            print(f"Запрос: {data[:200]}...")

            request = HTTPRequest(data)
            if self._handler:
                response = self._handler(request)
            else:
                response = HTTPResponse.internal_error()

            client_socket.send(response.to_bytes_str())
        except ConnectionResetError:
            print(f"разрыв соединения")
        except Exception as err:
            client_socket.send(HTTPResponse.internal_error().to_bytes_str())
            print(err)
        finally:
            client_socket.close()

    def _get_request(self, client_socket, buffer_size: int = 8192):

        client_socket.settimeout(5.0)

        data_parts = []
        while True:
            try:
                data = client_socket.recv(buffer_size)
                if not data:
                    break
                data_parts.append(data.decode('utf-8'))
                if '\r\n\r\n' in data_parts[-1]:
                    break
            except socket.timeout:
                break

        return ''.join(data_parts)

    def _stop(self):
        self._running = False
        if self._server_socket:
            self._server_socket.close()
