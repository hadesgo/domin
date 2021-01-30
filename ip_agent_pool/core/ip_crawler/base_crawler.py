#!/usr/bin/python3
# -*- coding: utf-8 -*-
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

