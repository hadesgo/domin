#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
import threading
import pymysql
from model.ip_model import IpItem
from tool.log import logger
from model.web_item import DomainItem


class Mysql(object):
    def __init__(self):
        self.db = pymysql.connect(host="139.224.54.100", user="root", password="123", database="HADES")
        self.lock = threading.Lock()
        self.db.ping()

    def __del__(self):
        self.db.close()

    def insert(self, ipItem):
        count = 1
        sql = "INSERT INTO IP_Pool(IP_Address, \
              IP_Port, IP_Protocol, IP_Nick, IP_Speed, IP_Area, IP_Score) \
              VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (ipItem.ip, ipItem.port, ipItem.protocol, ipItem.nick_type, ipItem.speed, ipItem.area, ipItem.score)
        try:
            self.lock.acquire()
            self.db.ping(reconnect=True)
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            self.lock.release()
            cursor.close()
        except:
            self.db.rollback()
            count = 0
        if count == 1:
            logger.info("插入新的代理:{}".format(ipItem))
        else:
            logger.warning("已经存在的代理:{}".format(ipItem))

    def web_insert(self, domainitem):
        count = 1
        sql = "INSERT INTO Website_Information(domain_name, \
              ip, area, registrar_domain_id, registrar_whois_server, registrar_url, updated_date, creation_date, \
              registry_expiry_date, registrar, registrar_iana_id, registrar_abuse_contact_email, \
              registrar_abuse_contact_phone) \
              VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (domainitem.domain_name, domainitem.ip, domainitem.area, domainitem.registrar_domain_id,
               domainitem.registrar_whois_server, domainitem.registrar_url, domainitem.updated_date,
               domainitem.creation_date, domainitem.registry_expiry_date, domainitem.registrar,
               domainitem.registrar_iana_id, domainitem.registrar_abuse_contact_email,
               domainitem.registrar_abuse_contact_phone)
        try:
            self.lock.acquire()
            self.db.ping(reconnect=True)
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            self.lock.release()
            cursor.close()
        except:
            self.db.rollback()
            count = 0
        if count == 1:
            logger.info("插入新的网站信息:{}".format(domainitem))
        else:
            logger.warning("已经存在的网站信息:{}".format(domainitem))

    def find_web(self, url):
        sql = "SELECT * FROM Website_Information WHERE domain_name = '%s' " % \
              url
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            for item in results:
                domain = DomainItem(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8],
                                    item[9], item[10], item[11], item[12])
                return domain
            cursor.close()
        except:
            print("Error: unable to fetch data")

    def update_port(self, ipItem):
        sql = "UPDATE IP_Pool SET IP_Port = '%s' where IP_Address = '%s' " % \
              (ipItem.port, ipItem.ip)
        try:
            self.lock.acquire()
            self.db.ping(reconnect=True)
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            self.lock.release()
            cursor.close()
        except:
            self.db.rollback()

    def update_protocol(self, ipItem):
        sql = "UPDATE IP_Pool SET IP_Protocol = '%s' where IP_Address = '%s' " % \
              (ipItem.protocol, ipItem.ip)
        try:
            self.lock.acquire()
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            self.lock.release()
            cursor.close()
        except:
            self.db.rollback()

    def update_nick(self, ipItem):
        sql = "UPDATE IP_Pool SET IP_Nick = '%s' where IP_Address = '%s' " % \
              (ipItem.nick_type, ipItem.ip)
        try:
            self.lock.acquire()
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            self.lock.release()
            cursor.close()
        except:
            self.db.rollback()

    def update_speed(self, ipItem):
        sql = "UPDATE IP_Pool SET IP_Speed = '%s' where IP_Address = '%s' " % \
              (ipItem.speed, ipItem.ip)
        try:
            self.lock.acquire()
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            self.lock.release()
            cursor.close()
        except:
            self.db.rollback()

    def update_score(self, ipItem):
        count = 1
        sql = "UPDATE IP_Pool SET IP_Score = '%s' where IP_Address = '%s' " % \
              (ipItem.score, ipItem.ip)
        try:
            self.lock.acquire()
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            self.lock.release()
            cursor.close()
        except:
            self.db.rollback()
            count = 0
        if count == 1:
            logger.info("修改代理成功:{}".format(ipItem))
        else:
            logger.warning("修改代理失败:{}".format(ipItem))

    def delete(self, ipItem):
        sql = "DELETE FROM IP_Pool WHERE IP_Address = '%s' " % \
              ipItem.ip
        try:
            self.lock.acquire()
            self.db.ping(reconnect=True)
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            self.lock.release()
            cursor.close()
        except:
            self.db.rollback()

    def find_all(self):
        sql = "SELECT * FROM IP_Pool"
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            for item in results:
                ip = IpItem(item[0], item[1], item[2], item[3], item[4], item[5], item[6])
                yield ip
            cursor.close()
        except:
            print("Error: unable to fetch data")

    def random(self, protocol):
        sql = "SELECT * FROM IP_Pool WHERE Ip_Protocol = '%s' or Ip_Protocol = 2" % \
              protocol
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            results = cursor.fetchall()
            item = random.choice(results)
            cursor.close()
            return item
        except:
            print("Error: don't get a proxy")


if __name__ == '__main__':
    mysql = Mysql()
    ip = mysql.random(0)
    print(ip[1])
