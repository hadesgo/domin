#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gevent.monkey

from ip_agent_pool import settings
from queue import Queue
from ip_agent_pool.core.db.mysql_pool import *
from ip_agent_pool.core.ip_check.httpbin_check import check_proxy
from ip_agent_pool.tool.log import logger
import schedule
import time
from gevent.pool import Pool
gevent.monkey.patch_all()


class ProxyTester(object):
    def __init__(self):
        self.queue = Queue()
        self.pool = Pool()
        self.proxy_pool = Mysql()

    def _test_proxy(self):
        proxy = self.queue.get()
        try:
            proxy = check_proxy(proxy)
            if proxy.speed == -1:
                proxy.score -= 1
                if proxy.score == 0:
                    self.proxy_pool.delete(proxy)
                    logger.info('删除代理:{}'.format(proxy))
                else:
                    self.proxy_pool.update_score(proxy)
            else:
                proxy.score = settings.MAX_SCORE
                self.proxy_pool.update_score(proxy)

        except Exception as ex:
            logger.exception(ex)

        self.queue.task_done()

    def _test_proxy_finish(self, temp):
        self.pool.apply_async(self._test_proxy, callback=self._test_proxy_finish)

    def run(self):
        # 1. 获取所有代理IP
        proxies = self.proxy_pool.find_all()
        # 2. 如果代理池为空, 直接返回
        if proxies is None:
            print("代理池为空")
            return

        # 获取所有的代理, 放到队列中
        for proxy in proxies:
            self.queue.put(proxy)

        # 开启多个异步任务执行检查IP的任务
        for i in range(settings.TESTER_ANSYC_COUNT):
            self.pool.apply_async(self._test_proxy, callback=self._test_proxy_finish)

        # 让主线程等待异步任务完成
        self.queue.join()

    @staticmethod
    def start():
        tester = ProxyTester()
        tester.run()
        schedule.every(settings.TESTER_INTERVAL).hours.do(tester.run)
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    ProxyTester.start()
