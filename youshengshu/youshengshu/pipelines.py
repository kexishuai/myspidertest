# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class YoushengshuPipeline(object):

    # 保存为json文件
    def open_spider(self, spider):
        self.fp = open('yousheng.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        d = dict(item)
        string = json.dumps(d, ensure_ascii=False)
        self.fp.write(string + '\n')
        return item

    def close_spider(self, spider):
        self.fp.close()

# 存储至mysql
import pymysql
from scrapy.utils.project import get_project_settings

class YoushengMysqlPipeline(object):
    def open_spider(self, spider):
        # 读取配置文件中的配置信息
        settings = get_project_settings()
        host = settings['HOST']
        port = settings['PORT']
        user = settings['USER']
        password = settings['PASSWORD']
        dbname = settings['DBNAME']
        charset = settings['CHARSET']
        # 链接数据库
        self.conn = pymysql.connect(host=host, port=port, user=user, password=password, db=dbname, charset=charset)
        # 获取游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # 执行sql语句，写入到数据库中
        # 拼接sql语句

        # 爬取所有
        # sql = 'insert into youshengshu(img_url, book_name, book_author, detail_url, hot, detail_img_src, detail_book_name, update_time, book_type, book_intro) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(item['img_url'], item['book_name'], item['book_author'], item['detail_url'],item['hot'],item['detail_img_src'],item['detail_book_name'],item['update_time'],item['book_type'],item['book_intro'])

       # 仅仅爬取音频和书名
        sql = 'insert into shu_detail(book_name,detail_url,title,audio_url) values("%s","%s","%s","%s")'%(item['book_name'], item['detail_url'], item['title'], item['audio_url'])

        try:
            self.cursor.execute(sql)
            # 提交一下
            self.conn.commit()
        except Exception as e:
            print('*' * 100)
            print(e)
            print('*' * 100)
            # 回滚
            self.conn.rollback()
        return item

        # 执行sql语句

    def close_spider(self, spider):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库
        self.conn.close()


