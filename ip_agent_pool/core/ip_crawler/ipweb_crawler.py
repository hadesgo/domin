import requests
import re
import js2py

from ip_agent_pool.core.ip_crawler.base_crawler import *
from ip_agent_pool.tool.http import *
from ip_agent_pool.ip_model import *


class Ip3366Crawler(BaseCrawler):
    urls = ['http://www.ip3366.net/free/?stype={}&page={}'.format(i, j) for j in range(1, 10) for i in range(1, 4, 2)]
    group_xpath = '//*[@id="list"]/table/tbody/tr'
    detail_xpath = {'ip': './td[1]/text()', 'port': './td[2]/text()', 'area': './td[5]/text()'}


class ProxylistplusCrawler(BaseCrawler):
    urls = ['https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}'.format(i) for i in range(1, 7)]
    group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'
    detail_xpath = {'ip': './td[2]/text()', 'port': './td[3]/text()', 'area': './td[5]/text()'}


class Ip66Crawler(BaseCrawler):
    urls = ['http://www.66ip.cn/{}.html'.format(i) for i in range(1, 10)]
    group_xpath = '//*[@id="main"]/div/div[1]/table/tr[position()>1]'
    detail_xpath = {'ip': './td[1]/text()', 'port': './td[2]/text()', 'area': './td[3]/text()'}

    def get_page_from_url(self, url):
        """发送请求, 获取响应的方法"""
        # 获取session对象, session可以记录服务器设置过来的cookie信息
        session = requests.session()
        session.headers = getuser_agent()
        respsone = session.get(url)
        # 如果响应码是521
        if respsone.status_code == 521:
            # 通过正则获取, 需要执行的js
            rs = re.findall('window.onload=setTimeout\("(\w+\(\d+\))", \d+\); (function \w+\(\w+\).+?)</script>',
                            respsone.content.decode())
            # 获取js2py的js执行环境
            context = js2py.EvalJs()

            # 把执行执行js, 修改为返回要执行的js
            func = rs[0][1].replace('eval("qo=eval;qo(po);");', 'return po;')
            # 让js执行环境, 加载要执行的js
            context.execute(func)
            # 把函数的执行结果赋值给一个变量
            context.execute("a={}".format(rs[0][0]))
            # 从变量中取出cookie信息
            cookie = re.findall("document.cookie='(\w+)=(.+?);", context.a)
            # 把从js中提取的cookie信息设置给session
            session.cookies[cookie[0][0]] = cookie[0][1]
            # print(session.cookies)
            respsone = session.get(url)

        return respsone.content.decode('gbk')


if __name__ == '__main__':
    spider = ProxylistplusCrawler()
    for proxy in spider.get_ipitem():
        print(proxy)
