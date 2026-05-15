#!/usr/bin/env python3

import socket
import sys
import threading


class Server:

    def __init__(self, host='0.0.0.0', port=10000):
        self.host = host
        self.port = port
        self.server_socket = None
        self.dictionary = {}


    def start(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            print("сервер запущен")

            self.server_socket.listen(5)

            while True:
                client_socket, client_address = self.server_socket.accept()
                self.serve_client(client_socket)

        except KeyboardInterrupt:
            print(f"остановка пользователем сервера")
        except Exception as err:
            print(err)
        finally:
            self.stop()

    def serve_client(self, client_socket):

        try:
            #ожидание данных от клиента
            client_socket.settimeout(5.0)

            while True:
                try:
                    data = client_socket.recv(4096)
                    if not data:
                        break

                    request = data.decode('utf-8').strip()
                    if not request:
                        continue

                    response = self.handle_command(request)
                    if response:
                        client_socket.send(response.encode('utf-8'))

                except socket.timeout:
                    continue
                except ConnectionResetError:
                    print("разорвано соединение клиентом")
                    break
                except Exception as err:
                    break
        finally:
            client_socket.close()

    def handle_command(self, request):

        if not request:
            return ""

        request_parts = request.split(maxsplit=2)

        if not request_parts:
            return "пустая команда\n"

        command = request_parts[0].upper()

        if command == 'W':
            if len(request_parts) != 3:
                return "W <key> <data> - запись значения <data> в словарь по ключу <key>.\n"

            key = request_parts[1]
            data = request_parts[2]

            self.dictionary[key] = data
            return "OK\n"

        elif command == 'R':
            if len(request_parts) != 2:
                return "R <key> - чтение значения из словарь по ключу <key>.\n"

            key = request_parts[1]

            if key in self.dictionary:
                return f"{self.dictionary[key]}\n"
            else:
                return "ключ не найден\n"

        else:
            return f"неизвестная команда {command}\n"

    def stop(self):
        if self.server_socket:
            self.server_socket.close()


