import pymysql
import random
from ip_agent_pool.settings import *
from ip_agent_pool.tool.log import logger
from ip_agent_pool.ip_model import IpItem


class Mysql(object):
    def __init__(self):
        self.db = pymysql.connect(host="139.224.54.100", user="root", password="123", database="HADES")
        self.cursor = self.db.cursor()

    def __del__(self):
        self.db.close()

    def insert(self, ipItem):
        count = 1
        sql = "INSERT INTO IP_Pool(IP_Address, \
              IP_Port, IP_Protocol, IP_Nick, IP_Speed, IP_Area, IP_Score) \
              VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % \
              (ipItem.ip, ipItem.port, ipItem.protocol, ipItem.nick_type, ipItem.speed, ipItem.area, ipItem.score)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()
            count = 0
        if count == 1:
            logger.info("插入新的代理:{}".format(ipItem))
        else:
            logger.warning("已经存在的代理:{}".format(ipItem))

    def update_port(self, ipItem):
        sql = "UPDATE IP_Pool SET IP_Port = %s where IP_Address = %s " % \
              (ipItem.port, ipItem.ip)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def update_protocol(self, ipItem):
        sql = "UPDATE IP_Pool SET IP_Protocol = %s where IP_Address = %s " % \
              (ipItem.protocol, ipItem.ip)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def update_nick(self, ipItem):
        sql = "UPDATE IP_Pool SET IP_Nick = %s where IP_Address = %s " % \
              (ipItem.nick_type, ipItem.ip)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def update_speed(self, ipItem):
        sql = "UPDATE IP_Pool SET IP_Speed = %s where IP_Address = %s " % \
              (ipItem.speed, ipItem.ip)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def update_score(self, ipItem):
        sql = "UPDATE IP_Pool SET IP_Score = %s where IP_Address = %s " % \
              (ipItem.score, ipItem.ip)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def delete(self, ipItem):
        sql = "DELETE FROM IP_Pool WHERE IP_Address = %s " % \
              ipItem.ip
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

    def find_all(self):
        sql = "SELECT * FROM IP_Pool"
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for item in results:
                print(item)
        except:
            print("Error: unable to fetch data")


if __name__ == '__main__':
    mysql = Mysql()
    ipitem = IpItem('202.104.113.35', '53281')
    mysql.insert(ipitem)
    mysql.find_all()
