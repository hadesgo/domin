#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

from ip_agent_pool.core.db.mysql_pool import Mysql


class ProxyApi(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.proxy_pool = Mysql()

        @self.app.route('/random')
        def random():
            protocol = request.args.get('protocol')
            proxy = self.proxy_pool.random(protocol=protocol)
            print(protocol)
            if protocol:
                return '{}://{}:{}'.format(protocol, proxy.ip, proxy.port)
            else:
                return '{}:{}'.format(proxy.ip, proxy.port)

    def run(self):
        self.app.run(host='0.0.0.0', port=6868)

    @classmethod
    def start(cls):
        proxy_api = cls()
        proxy_api.run()


if __name__ == '__main__':
    ProxyApi.start()
