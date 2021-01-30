#!/usr/bin/python3
# -*- coding: utf-8 -*-
from web_crawler import *
from db.mysql_pool import Mysql


class RunWeb(object):
    def __init__(self, url):
        self.mysql = Mysql()
        self.web_crawler = WebCrawler(url)
