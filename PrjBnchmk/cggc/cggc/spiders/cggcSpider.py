# -*- coding: utf-8 -*-
import scrapy
import requests
from urllib.parse import urlencode
import bs4
from ..items import CggcItem
import logging
logger = logging.getLogger(__name__)


class CggcspiderSpider(scrapy.Spider):
    name = 'cggcSpider'
    allowed_domains = ['gzbgj.com']
    start_urls = ['http://www.gzbgj.com/col/col7615/index.html']
    start = 1
    end = start + 59

    def start_req(self):
        """
        进行url拼接
        :param start:
        :param end:
        :return:
        """
        home_urls = 'http://www.gzbgj.com/module/jslib/jquery/jpage/dataproxy.jsp?'
        data = {
            "startrecord": self.start,
            "endrecord": self.end,
            "perpage": 20,
        }
        params = urlencode(data)
        url = home_urls + params
        print(url)
        return url

    def parse(self, response):
        keyword = "签约"
        # 构造request的url

        url = self.start_req()
        # 构造request post form data
        data = "appid=1&webid=27&path=%2F&columnid=7615&sourceContentType=1&unitid=56554&webname=%E4%B8%AD%E5%9B%BD%E8%91%9B%E6%B4%B2%E5%9D%9D%E9%9B%86%E5%9B%A2%E5%9B%BD%E9%99%85%E5%B7%A5%E7%A8%8B%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&permissiontype=0"
        # 构造请求header
        header = {
            'Accept': 'text/javascript, application/javascript, */*',
            'Accept- Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-length': '233',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'JSESSIONID=E59F8413AE771F7B79A9A0E12EEC7B80; acw_tc=7b39758715821845337757109ea8a2879399902f7a4d85847fb64e2484d02b',
            'Host': 'www.gzbgj.com',
            'Origin': 'http://www.gzbgj.com',
            'Referer': 'http://www.gzbgj.com/col/col7615/index.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        session = requests.Session()
        session.trust_env = False
        # 提出post请求抓取数据
        response = session.post(url, headers=header, data=data)
        # 打印请求状态
        print(response.status_code)
        # 对数据进行解码
        content = bs4.BeautifulSoup(response.content.decode("utf8"), "lxml")

        # 关键字查找
        filter_result = content.find_all(lambda e: e.name == 'a' and keyword in e.text)
        # 进行提取和匹配title和publish_date
        for result in filter_result:
            item = CggcItem()
            item['title'] = result.string
            item['href'] = result.get('href')[2:-2]
            # Detail页的url拼接
            item['href'] = "http://www.gzbgj.com" + item['href']
            date = result.parent.find_next_sibling()
            item['publish_date'] = date.string
            # print(item)
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"items": item},
            )
        #  进行翻页操作
        if self.start <= 60:
            # 翻页
            self.start += 60
            self.end += 60
            next_url = url
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            logger.warning('fail to next page')

    def parse_detail(self, response):
        item = response.meta["items"]
        item["content"] = response.xpath("//tr/td[@class='bt_content']/div//p/text()").extract_first()
        item["content_img"] = response.xpath("//tr/td[@class='bt_content']/div//p/img/@src").extract()
        item["content_img"] = ["www.gzbgj.com" + i for i in item["content_img"]]
        yield item
