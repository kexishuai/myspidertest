# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JingdongPipeline(object):
    def process_item(self, item, spider):
        return item

import pymongo
from scrapy.conf import settings

class jingdongMongodbPipeline(object):

    def __init__(self):
        # 获取setting主机名、端口号和数据库名称
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DBNAME']

        # 创建数据库连接
        client = pymongo.MongoClient(host=host,port=port)

        # 指向指定数据库
        mdb = client[dbname]

        # 获取数据库里面存放数据的表名
        self.post = mdb[settings['MONGODB_DOCNAME']]

    def process_item(self, item, spider):
        data = dict(item)
        # 向指定的表里添加数据
        self.post.insert(data)
        return item