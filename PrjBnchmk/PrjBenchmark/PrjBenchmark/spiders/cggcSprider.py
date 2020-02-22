# -*- coding: utf-8 -*-
import scrapy
import logging
import json
from PrjBenchmark.items import PrjbenchmarkItem


logger = logging.getLogger(__name__)


class CggcspriderSpider(scrapy.Spider):
    name = 'cggcSprider'
    allowed_domains = ['gzbgj.com']
    start_urls = ['http://www.gzbgj.com/col/col7615/index.html']

    # 列表页处理数据
    def parse(self, response):
        # 新闻标题行所在的位置：tr里
        tr_list = response.xpath("//div[@id=56554]/div/table//tr")
        for tr in tr_list:
            items = PrjbenchmarkItem()
            items["title"] = tr.xpath("./td[1]/a[@class='new_link1']/@title").extract_first()
            items["href"] = tr.xpath("./td[1]/a[@class='new_link1']/@href").extract_first()
            items["href"] = response.urljoin(items["href"])
            items["publish_date"] = tr.xpath("./td[2]/text()").extract_first()
            yield scrapy.Request(
                items["href"],
                callback=self.parse_detail,
                meta={"items": items}
            )

        # 翻页操作，对于使用Ajax动态加载的翻页
        # 使用Post 进行翻页操作
        # 一种是Form_Data进行改变，一种是Query String Parameter进行改变
        # 但是我这里抓不到东西啊！！！
        n = len(tr_list)
        print(n)
        if n == 60:
            print(n+1)
            # 这个request url应该有问题
            next_url = "http://www.gzbgj.com/module/jslib/jquery/jpage/dataproxy.jsp?startrecord=61&endrecord=120&perpage=20"
            form_data = {
                'appid': '1',
                'webid': '27',
                'path': '/',
                'columnid': '7651',
                'sourceContentType': '1',
                'unitid': '56554',
                'webname': '中国葛洲坝集团国际工程有限公司',
                'permissiontype': '0',
            }
            # yield scrapy.Request(
            #     next_url,
            #     method="POST",
            #     data=json.dumps(data),
            #     callback=self.parse
            # )

            yield scrapy.FormRequest(next_url, formdata=form_data)
        else:
            pass

    def parse_detail(self, response):
        items = response.meta["items"]
        logger.warning(items)
        pass
