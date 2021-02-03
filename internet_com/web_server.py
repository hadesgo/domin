#!/usr/bin/python3
# -*- coding: utf-8 -*-
import socket
import sys
from Website_information.web_run import RunWeb


class WebServer(object):
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = socket.gethostname()
        self.port = 9999

    def connection(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        while True:
            client_socket, addr = self.server_socket.accept()
            print("连接地址: %s" % str(addr))
            url = client_socket.recv(1024)
            web_run = RunWeb(url.decode('utf-8'))
            web_msg, web_port = web_run.run()
            web_msg = str(web_msg)
            web_port = str(web_port)
            client_socket.send(web_msg.encode('utf-8'))
            client_socket.send(web_port.encode('utf-8'))
            client_socket.close()

    @classmethod
    def start(cls):
        web_server = WebServer()
        web_server.connection()


if __name__ == '__main__':
    WebServer.start()
