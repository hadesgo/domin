# -*- coding: utf-8 -*-
"""
@File    :   ip_model.py
@Time    :   2020/11/14 20:51:16
@Author  :   hades-li
"""
from ip_agent_pool.settings import MAX_SCORE


# IP代理模型类，用于封装代理IP的各种信息
class IpItem(object):
    def __init__(self, ip, port, protocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE):
        self.ip = ip  # ip
        self.port = port  # 端口号
        self.protocol = protocol  # 代理ip支持的协议的类型，仅支持HTTP为0，仅支持HTTPS为1，两者都支持为2
        self.nick_type = nick_type  # 代理ip的匿名程度，透明为0，普通为1，高匿为2
        self.speed = speed  # 代理ip响应的速度，单位为s
        self.area = area  # 代理ip所在地区
        self.score = score  # 代理ip的评分，初始评分为50。若ip响应失败则扣1分，扣至0分则移除ip池中

    def __str__(self):
        # 返回数据字符串
        return str(self.__dict__)
