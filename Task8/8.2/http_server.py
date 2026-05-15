#!/usr/bin/env python3

import socket
import sys
from typing import Callable, Optional

from http_request import HTTPRequest
from http_response import HTTPResponse


class HTTPServer:
    def __init__(self, host: str = '0.0.0.0', port: int = 10000):
        self.host = host
        self.port = port
        self._server_socket: Optional[socket.socket] = None
        self._running = False
        self._handler: Optional[Callable[[HTTPRequest], HTTPResponse]] = None

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
            print(f"Сервер остановлен пользователем")
        except Exception as err:
            print(err)
        finally:
            self._stop()

    def _create_server_socket(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind((self.host, self.port))
        self._server_socket.listen(5)

    def _handle_client(self, client_socket: socket.socket):

        try:
            request_data = self._receive_request(client_socket)
            if not request_data:
                return

            print(f"Запрос: {request_data[:200]}...")

            # Парсим запрос
            request = HTTPRequest(request_data)

            # Обрабатываем запрос через установленный handler
            if self._handler:
                response = self._handler(request)
            else:
                response = HTTPResponse.internal_error()

            # Отправляем ответ
            client_socket.send(response.to_bytes())
            print(f"Ответ отправлен: {response.status_code}")

        except ConnectionResetError:
            print(f"Клиент разорвал соединение")
        except Exception as e:
            print(f"Ошибка обработки запроса: {e}", file=sys.stderr)
            try:
                client_socket.send(HTTPResponse.internal_error().to_bytes())
            except:
                pass
        finally:
            client_socket.close()

    def _receive_request(self, client_socket: socket.socket, buffer_size: int = 8192) -> str:

        client_socket.settimeout(5.0)

        data_parts = []
        while True:
            try:
                data = client_socket.recv(buffer_size)
                if not data:
                    break
                data_parts.append(data.decode('utf-8'))

                # Проверяем, получили ли мы полный запрос
                if '\r\n\r\n' in data_parts[-1]:
                    break
            except socket.timeout:
                break

        return ''.join(data_parts)

    def _stop(self):
        self._running = False
        if self._server_socket:
            self._server_socket.close()

    def stop(self):
        self._stop()