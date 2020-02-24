# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import re
from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class PrjbenchmarkPipeline(object):
    def process_item(self, item, spider):
        # Note：在进入pipeline之后空的item就自动被拿掉了
        item["content"] = self.process_content(item["content"])
        print(item["content"])
        print(type(item["content"]))
        if spider.name == "ceecTest":
            logger.warning("-" * 10)
        else:
            pass
        logger.warning(item)
        return item

    def process_content(self, content):
        """
        对抓取的content进行处理：去除空格，\xa0,\
        用re库对文字进行处理
        :param content:
        :return:
        """
        content = re.sub(r"\xa0", r"", content)
        # content = content if len(content) > 0 # 去除列表中的空字符串
        return content
