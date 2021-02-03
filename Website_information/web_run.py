#!/usr/bin/python3
# -*- coding: utf-8 -*-
from Website_information.web_crawler import WebCrawler
from db.mysql_pool import Mysql
from port_scanning.ProtScanning import PortWorker


class RunWeb(object):
    def __init__(self, url, top=1000):
        self.url = url
        self.top = top
        self.mysql = Mysql()
        self.web_crawler = WebCrawler(self.url)
        self.port_scanner = PortWorker(self.url, self.top)

    def check_rul(self):
        msg = self.mysql.find_web(self.url)
        if msg is not None:
            return msg
        else:
            self.web_crawler.run()
        msg = self.mysql.find_web(self.url)
        return msg

    def check_port(self):
        msg = self.port_scanner.run()
        return msg

    def run(self):
        web_information = self.check_rul()
        web_port = self.check_port()
        return web_information, web_port


if __name__ == '__main__':
    run_web = RunWeb("www.kugou.com")
    web_msg, web_port = run_web.run()
    print(web_msg)
    print(web_port)
