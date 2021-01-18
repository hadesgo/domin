# -*- coding: utf-8 -*-
"""
@File    :   httpbin_check.py
@Time    :   2020/11/15 20:01:01
@Author  :   hades-li
"""
import json
import time

import requests

from ip_agent_pool.ip_model import *
from ip_agent_pool.settings import *
from ip_agent_pool.tool.http import *
from ip_agent_pool.tool.log import logger


def check_proxy(iPitem):
    """
    检测代理协议类型, 匿名程度
    :param
    :return:(协议: http和https:2,https:1,http:0, 匿名程度:高匿:0,匿名: 1, 透明:0 , 速度, 单位s )
    """

    # 根据proxy对象构造, 请求使用的代理
    proxies = {
        'http': "http://{}:{}".format(iPitem.ip, iPitem.port),
        'https': "https://{}:{}".format(iPitem.ip, iPitem.port),
    }

    http, http_nick_type, http_speed = check_http_ip(proxies)
    https, https_nick_type, https_speed = check_http_ip(proxies, False)
    if http and https:
        # 如果http 和 https 都可以请求成功, 说明支持http也支持https, 协议类型为2
        iPitem.protocol = 2
        iPitem.nick_type = http_nick_type
        iPitem.speed = http_speed
    elif http:
        # 如果只有http可以请求成功, 说明支持http协议, 协议类型为 0
        iPitem.protocol = 0
        iPitem.nick_type = http_nick_type
        iPitem.speed = http_speed
    elif https:
        # # 如果只有https可以请求成功, 说明支持https协议, 协议类型为 1
        iPitem.protocol = 1
        iPitem.nick_type = https_nick_type
        iPitem.speed = https_speed
    else:
        iPitem.protocol = -1
        iPitem.nick_type = -1
        iPitem.speed = -1

    logger.debug(iPitem)
    return iPitem


def check_http_ip(proxies, isHttp=True):
    nick_type = -1  # 匿名程度
    speed = -1  # 响应速度
    if isHttp:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'
    try:
        start = time.time()
        r = requests.get(test_url, headers=getuser_agent(), proxies=proxies, timeout=TIMEOUT)
        if r.ok:
            # 计算响应速度, 保留两位小数
            speed = round(time.time() - start, 2)
            # 把响应内容转换为字典
            content = json.loads(r.text)
            # 获取origin, 请求来源的IP地址
            ip = content["origin"]
            # 获取请求头中 `Proxy-Connection` 如果有, 说明匿名代理
            proxy_connection = content['headers'].get('Proxy-Connection', None)
            if ',' in ip:
                # 如果 `origin` 中有','分割的两个IP就是透明代理IP
                nick_type = 2  # 透明
            elif proxy_connection:
                # 如果 `headers` 中包含 `Proxy-Connection` 说明是匿名代理IP
                nick_type = 1  # 匿名
            else:
                #  否则就是高匿代理IP
                nick_type = 0  # 高匿
            return True, nick_type, speed
        else:
            return False, nick_type, speed
    except Exception as e:
        return False, nick_type, speed


if __name__ == '__main__':
    proxy = IpItem('103.115.14.41', '80')
    print(check_proxy(proxy))
