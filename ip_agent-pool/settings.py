# !/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@File    :   setting.py
@Time    :   2020/11/14 21:12:50
@Author  :   hades-li
'''
# 默认分数: 用于配置代理IP的最大评分,
# 在进行代理可用性检查的时候, 每遇到一次请求失败就减1份, 减到0的时候从池中删除. 如果检查代理可用, 就恢复默认分值
MAX_SCORE = 50

#日志配置信息
import logging

# 默认的配置
LOG_LEVEL = logging.INFO    # 默认等级
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'   # 默认日志格式
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
LOG_FILENAME = 'log.log'    # 默认日志文件名称