# -*- coding: utf-8 -*-
"""
@File    :   setting.py
@Time    :   2020/11/14 21:12:50
@Author  :   hades-li
"""
# 日志配置信息
import logging

# 默认分数: 用于配置代理IP的最大评分,
# 在进行代理可用性检查的时候, 每遇到一次请求失败就减1份, 减到0的时候从池中删除. 如果检查代理可用, 就恢复默认分值
MAX_SCORE = 50

# 默认的配置
LOG_LEVEL = logging.DEBUG  # 默认等级
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'   # 默认日志格式
LOG_DATETIME = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
LOG_FILENAME = 'log.log'  # 默认日志文件名称

# 设置超时时间
TIMEOUT = 10

# 配置代理爬虫列表
PROXIES_CRAWLER = [
    'ip_crawler.ipweb_crawler.Ip66Crawler',
    'ip_crawler.ipweb_crawler.Ip3366Crawler',
    'ip_crawler.ipweb_crawler.ProxylistplusCrawler',
]

# 抓取IP的时间间隔，单位小时
CRAWLER_INTERVAL = 2

# 异步
TESTER_ANSYC_COUNT = 10

# 检查可用IP的时间间隔，单位小时
TESTER_INTERVAL = 1

