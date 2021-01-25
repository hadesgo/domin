from multiprocessing import Process
from ip_agent_pool.core.ip_crawler.run_crawler import RunCrawler
from ip_agent_pool.core.ip_api import ProxyApi
from ip_agent_pool.core.ip_test import ProxyTester


def run():
    process_list = [Process(target=RunCrawler.start, name='run_crawler'),
                    Process(target=ProxyTester.start, name='run_tester'),
                    Process(target=ProxyApi.start, name='run_api')]

    for p in process_list:
        p.daemon = True
        p.start()

    for p in process_list:
        p.join()


if __name__ == '__main__':
    run()
