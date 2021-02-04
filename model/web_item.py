#!/usr/bin/python3
# -*- coding: utf-8 -*-

class DomainItem(object):
    def __init__(self, domain_name, ip, area=None, registrar_domain_id=None, registrar_whois_server=None,
                 registrar_url=None, updated_date=None, creation_date=None, registry_expiry_date=None, registrar=None,
                 registrar_iana_id=None, registrar_abuse_contact_email=None, registrar_abuse_contact_phone=None):
        self.domain_name = domain_name  # 域名
        self.ip = ip  # ip
        self.area = area  # 地区
        self.registrar_domain_id = registrar_domain_id  # 注册域ID
        self.registrar_whois_server = registrar_whois_server  # 注册服务商WHOIS服务器
        self.registrar_url = registrar_url  # 注册服务商URL
        self.updated_date = updated_date  # 更新日期
        self.creation_date = creation_date  # 创建日期
        self.registry_expiry_date = registry_expiry_date  # 注册服务商注册到期日期
        self.registrar = registrar  # 注册服务商
        self.registrar_iana_id = registrar_iana_id  # 注册服务商IANA ID
        self.registrar_abuse_contact_email = registrar_abuse_contact_email  # 注册服务商邮箱
        self.registrar_abuse_contact_phone = registrar_abuse_contact_phone  # 注册服务商电话

    def __str__(self):
        # 返回数据字符串
        return str(self.__dict__)
