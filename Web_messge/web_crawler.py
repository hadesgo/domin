from bs4 import BeautifulSoup
import requests
import re
from ip_agent_pool.tool.http import getuser_agent


class WebCrawler(object):
    def __init__(self, url, ip):
        self.url = url
        self.ip = ip

    def askUrl(self):
        head = getuser_agent()
        html = ""
        try:
            response = requests.get(self.url, headers=head, proxies=self.ip, timeout=1)
            response.encoding = 'utf-8'
            html = response.text
        except Exception as e:
            print(e)
        return html

    def getData(self):
        html = self.askUrl()
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
        domain_name = re.findall(find_domain_name, item)[0]
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
