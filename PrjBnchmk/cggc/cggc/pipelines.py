# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import re
import sqlite3
# from scrapy.exceptions import DropItem

logger = logging.getLogger(__name__)


class CggcPipeline(object):
    # 打开数据库
    def open_spider(self, spider):
        db_name = spider.settings.get('SQLITE_DB_NAME', 'cggc.db')
        # 连接数据库
        self.db_conn = sqlite3.connect(db_name)
        # 创建一个数据库的cursor
        self.db_cur = self.db_conn.cursor()
        print("open database successfully" + "-"*10)

    def close_spider(self, spider):
        self.db_conn.close()
        print("close database successfully" + "*" * 10)

    def process_item(self, item, spider):
        # 对提取出来的content进行处理
        item["content"] = self.process_content(item["content"])
        if spider.name == "cggcSpider":
            logger.warning("--|" * 10)
        else:
            logger.warning("**" * 10)
        logger.warning(item)
        # 将处理数据写入数据库
        self.insert_db(item)
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

    def insert_db(self, item):
        insert_sql = "INSERT INTO cggc (title, publish_date, content) " \
                     "VALUES('{}', '{}' ,'{}')".format(item['title'], item['publish_date'], item['content'])

        self.db_cur.execute('CREATE TABLE IF NOT EXISTS cggc '
                            '(title, publish_date, content, content_img)')
        # print(insert_sql)
        self.db_cur.execute(insert_sql)
        self.db_conn.commit()
