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
    # start_record = 1
    # end_record = 60
    # per_page = 20

    # 列表页提取 1. title 2. href 3. publish_date
    def parse(self, response):
        # 新闻标题行所在的位置：tr里
        # filter_item = []
        keyword = "签约"
        tr_list = response.xpath("//div[@id=56554]/div/table//tr")
        for tr in tr_list:
            item = PrjbenchmarkItem()
            item["title"] = tr.xpath("./td[1]/a[@class='new_link1']/@title").extract_first()

            # 关键字过滤
            pos = item["title"].find(keyword)
            if pos != -1:
                print("找到1项")
                item["href"] = tr.xpath("./td[1]/a[@class='new_link1']/@href").extract_first()
                # href 进行拼接
                item["href"] = response.urljoin(item["href"])
                item["publish_date"] = tr.xpath("./td[2]/text()").extract_first()
                yield scrapy.Request(
                    item["href"],
                    callback=self.parse_detail,
                    meta={"items": item}
                )
            else:
                item.popitem()
            # print(item)

        # 翻页操作，对于使用Ajax动态加载的翻页
        # 使用Post 进行翻页操作
        # 一种是Form_Data进行改变，一种是Query String Parameter进行改变
        # 但是我这里抓不到东西啊！！！

        n = len(tr_list)
        print(n)
        if n == 60:
            # start_record += 60
            # end_record += 60
            print(n+1)
            # 这个request url应该有问题
            next_url = "http://www.gzbgj.com/module/jslib/jquery/jpage/dataproxy.jsp?startrecord={start_record}" \
                       "&endrecord={end_record}&perpage=20"
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
        """
        提取content和content_img
        提取出来的content需要进行处理
        用pipeline处理
        :param response:
        :return:
        """
        items = response.meta["items"]
        items["content"] = response.xpath("//tr/td[@class='bt_content']/div//p/text()").extract_first()
        items["content_img"] = response.xpath("//tr/td[@class='bt_content']/div//p/img/@src").extract()
        items["content_img"] = ["www.gzbgj.com"+i for i in items["content_img"]]

        yield items
        # logger.warning(items)
        pass
