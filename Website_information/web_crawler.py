#!/usr/bin/python3
# -*- coding: utf-8 -*-
import re
import socket

import requests
from bs4 import BeautifulSoup

from Website_information import web_item
from db.mysql_pool import Mysql
from ip_agent_pool.tool.http import getuser_agent


class WebCrawler(object):
    def __init__(self, url):
        self.url = url
        self.mysql = Mysql()
        self.ipItem = self.mysql.random(0)
        self.ip = None  # {'http': str(self.ipItem[0]) + ':' + str(self.ipItem[1])}
        self.head = getuser_agent()

    def ask_url(self):
        html = ""
        url = "http://whois.chinaz.com/" + self.url
        try:
            response = requests.get(url, headers=self.head, proxies=self.ip, timeout=1)
            response.encoding = 'utf-8'
            html = response.text
        except Exception as e:
            print(e)
        return html

    def get_data(self):
        html = self.ask_url()
        soup = BeautifulSoup(html, "html.parser")
        item = soup.find_all('p', class_="MoreInfo")
        item = str(item)
        find_domain_name = re.compile(r'Domain Name: (.*?)<br/>')
        find_registry_domain_id = re.compile(r'Registry Domain ID: (.*?)<br/>')
        find_registrar_whois_server = re.compile(r'Registrar WHOIS Server: (.*?)<br/>')
        find_registrar_url = re.compile(r'Registrar URL: (.*?)<br/>')
        find_updated_date = re.compile(r'Updated Date: (.*?)<br/>')
        find_creation_date = re.compile(r'Creation Date: (.*?)<br/>')
        find_registry_expiry_date = re.compile(r'Registry Expiry Date: (.*?)<br/>')
        find_registrar = re.compile(r'Registrar: (.*?)<br/>')
        find_registrar_iana_id = re.compile(r'Registrar IANA ID: (.*?)<br/>')
        find_registrar_abuse_contact_email = re.compile(r'Registrar Abuse Contact Email: (.*?)<br/>')
        find_registrar_abuse_contact_phone = re.compile(r'Registrar Abuse Contact Phone:(.*?)<br/>')
        # domain_name = re.findall(find_domain_name, item)[0]
        registrar_domain_id = re.findall(find_registry_domain_id, item)[0]
        registrar_whois_server = re.findall(find_registrar_whois_server, item)[0]
        registrar_url = re.findall(find_registrar_url, item)[0]
        updated_date = re.findall(find_updated_date, item)[0]
        creation_date = re.findall(find_creation_date, item)[0]
        registry_expiry_date = re.findall(find_registry_expiry_date, item)[0]
        registrar = re.findall(find_registrar, item)[0]
        registrar_iana_id = re.findall(find_registrar_iana_id, item)[0]
        registrar_abuse_contact_email = re.findall(find_registrar_abuse_contact_email, item)[0]
        registrar_abuse_contact_phone = re.findall(find_registrar_abuse_contact_phone, item)[0]
        ip = socket.gethostbyname(self.url)
        domain_name = self.url
        area = None
        item = web_item.DomainItem(domain_name, ip, area, registrar_domain_id, registrar_whois_server, registrar_url,
                                   updated_date, creation_date, registry_expiry_date, registrar, registrar_iana_id,
                                   registrar_abuse_contact_email, registrar_abuse_contact_phone)
        return item

    def save_data(self):
        item = self.get_data()
        self.mysql.web_insert(item)

    def run(self):
        self.save_data()


if __name__ == '__main__':
    web = WebCrawler("www.kugou.com")
    web.run()
