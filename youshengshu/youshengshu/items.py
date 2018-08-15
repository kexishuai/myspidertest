# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YoushengshuItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # img_url = scrapy.Field()
    book_name = scrapy.Field()
    # book_author = scrapy.Field()
    detail_url = scrapy.Field()
    # hot = scrapy.Field()
    #
    # detail_img_src = scrapy.Field()
    # detail_book_name = scrapy.Field()
    # update_time = scrapy.Field()
    # book_type = scrapy.Field()
    # book_intro = scrapy.Field()

    # 音频
    title = scrapy.Field()
    audio_url = scrapy.Field()

