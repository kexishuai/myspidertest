# -*- coding: utf-8 -*-
import json

import scrapy
from youshengshu.items import YoushengshuItem


class Red_sqlSpider(scrapy.Spider):
    name = 'red_sql'
    allowed_domains = ['www.ximalaya.com']

    start_urls = ['https://www.ximalaya.com/youshengshu/']

    page = 1
    page_url = 'https://www.ximalaya.com/youshengshu/p{}/'


    def parse(self, response):
        li_list = response.xpath('//div[@class="content"]/ul/li')
        for li in li_list:
            item = YoushengshuItem()

            book_name = li.xpath('./div/a')[0].xpath('string(.)').extract()[0]

            detail_url = 'https://www.ximalaya.com' + li.xpath('./div/a')[0].xpath('./@href').extract()[0]

            item['book_name']= book_name

            item['detail_url'] = detail_url

            yield scrapy.Request(url=detail_url,callback=self.parse_detail,meta={'item':item})

        # 页码,获取前5页
        if self.page <= 3:
            self.page += 1
            page_url = self.page_url.format(self.page)
            yield scrapy.Request(url=page_url,callback=self.parse)

    def parse_detail(self,response):
        item = response.meta['item']

        # print(response.url) # https://www.ximalaya.com/youshengshu/4137349/

        albumId = response.url.split('/')[-2]


        get_url = 'https://www.ximalaya.com/revision/album?albumId='+str(albumId)
        yield scrapy.Request(url=get_url,callback=self.parse_audio,meta={'item':item})

    def parse_audio(self,response):

        item = response.meta['item']

        # 获取接口数据

        res = response.body.decode('utf-8')
        dict_content = json.loads(res)
        audio_lists = dict_content['data']['tracksInfo']['tracks']

        for audio in audio_lists:
            try:
                item['title'] = audio['title']
                item['audio_url'] = 'https://www.ximalaya.com' + audio['url']
            except:
                item['title'] = ''
                item['audio_url'] = ''
            yield item