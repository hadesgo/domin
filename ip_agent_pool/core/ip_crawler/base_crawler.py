import requests
from lxml import etree
from ip_agent_pool.ip_model import *
from ip_agent_pool.tool.http import getuser_agent


class BaseCrawler(object):
    urls = []
    group_xpath = ''
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath=None, detail_xpath={}):
        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_page_from_url(self, url):
        response = requests.get(url, headers=getuser_agent())
        return response.content

    def get_first(self, lis):
        return lis[0].strip() if len(lis) != 0 else ''

    def get_ip_from_page(self, page):
        element = etree.HTML(page)
        trs = element.xpath(self.group_xpath)
        for tr in trs:
            ip = self.get_first(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first(tr.xpath(self.detail_xpath['port']))
            area = self.get_first(tr.xpath(self.detail_xpath['area']))
            ipitem = IpItem(ip, port, area=area)
            yield ipitem

    def get_ipitem(self):
        for url in self.urls:
            page = self.get_page_from_url(url)
            ipitem = self.get_ip_from_page(page)
            yield from ipitem


if __name__ == '__main__':
    config = {
        'urls': ['http://www.ip3366.net/free/?stype={}&page={}'.format(i, j) for j in range(1, 10) for i in
                 range(1, 4, 2)],
        'group_xpath': '//*[@id="list"]/table/tbody/tr',
        'detail_xpath': {'ip': './td[1]/text()', 'port': './td[2]/text()', 'area': './td[5]/text()'}
    }
    # 创建通用代理对象
    base_spider = BaseCrawler(**config)
    for proxy in base_spider.get_ipitem():
        print(proxy)
