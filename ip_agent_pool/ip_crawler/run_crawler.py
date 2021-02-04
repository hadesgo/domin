#!/usr/bin/python3
# -*- coding: utf-8 -*-
from gevent import monkey

monkey.patch_all()
from gevent.pool import Pool
import importlib
import schedule
import time

from settings import *
from ip_agent_pool.ip_check.httpbin_check import check_proxy
from db.mysql_pool import Mysql
from tool.log import logger


class RunCrawler(object):
    def __init__(self):
        self.pool = Pool()
        self.ip_pool = Mysql()

    def _auto_import_instances(self):
        instances = []
        for path in PROXIES_CRAWLER:
            module_name, cls_name = path.rsplit('.', maxsplit=1)
            module = importlib.import_module('ip_agent_pool.' + module_name)
            cls = getattr(module, cls_name)
            instances.append(cls())

        return instances

    def run(self):
        crawler = self._auto_import_instances()
        for cra in crawler:
            self.pool.apply_async(self.__run_one_crawler, args=(cra,))
        self.pool.join()

    def __run_one_crawler(self, cra):
        try:
            for proxy in cra.get_ipitem():
                if proxy is None:
                    continue
                proxy = check_proxy(proxy)
                if proxy.speed != -1:
                    self.ip_pool.insert(proxy)
        except Exception as e:
            logger.exception(e)
            logger.exception("爬虫{} 出现错误".format(cra))

    @classmethod
    def start(cls):
        run_crawler = RunCrawler()
        run_crawler.run()
        schedule.every(CRAWLER_INTERVAL).hours.do(run_crawler.run())
        while True:
            schedule.run_pending()
            time.sleep(1)

