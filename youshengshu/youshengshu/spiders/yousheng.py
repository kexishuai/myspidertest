# -*- coding: utf-8 -*-
import scrapy

from youshengshu.items import YoushengshuItem

class YoushengSpider(scrapy.Spider):
    name = 'yousheng'
    allowed_domains = ['www.ximalaya.com']

    start_urls = ['https://www.ximalaya.com/youshengshu/']


    page = 1
    page_url = 'https://www.ximalaya.com/youshengshu/p{}/'

    def parse(self, response):
        li_list = response.xpath('//div[@class="content"]/ul/li')
        for li in li_list:
            item = YoushengshuItem()
            img_url = li.xpath('./div/div/a/img/@src').extract()[0]
            book_name = li.xpath('./div/a')[0].xpath('string(.)').extract()[0]
            book_author = li.xpath('./div/a')[1].xpath('string(.)').extract()[0][3:]
            detail_url = 'https://www.ximalaya.com' + li.xpath('./div/a')[0].xpath('./@href').extract()[0]
            item['img_url'] = img_url
            item['book_name']= book_name
            item['book_author'] = book_author
            item['detail_url'] = detail_url

            yield scrapy.Request(url=detail_url,callback=self.parse_detail,meta={'item':item})

        # 页码,获取前5页
        if self.page <= 5:
            self.page += 1
            page_url = self.page_url.format(self.page)
            yield scrapy.Request(url=page_url,callback=self.parse)

    def parse_detail(self,response):
        item = response.meta['item']
        item['detail_img_src'] = response.xpath('//div[starts-with(@class,"detail")]//img/@src').extract()[0]
        item['detail_book_name'] = response.xpath('//div[starts-with(@class,"detail")]//h1/text()').extract()[0]
        item['update_time'] = response.xpath('//div[starts-with(@class,"detail")]//span[@class="e-630486218 time"]/text()').extract()[0]
        item['hot'] = response.xpath('//div[starts-with(@class,"detail")]//span[@class="e-630486218 count"]/text()').extract()[-1]
        item['book_type'] = response.xpath('//div[starts-with(@class,"detail")]//div[@class="e-630486218 tags"]').xpath('string(.)').extract()[0]
        try:
            item['book_intro'] = response.xpath('//article[@class="e-630486218 intro"]/p/span/text()').extract()[0]
        except Exception as e :
            item['book_intro'] = ''

        yield item
        # print(response.url) # https://www.ximalaya.com/youshengshu/4137349/

        # albumId = response.url.split('/')[-2]

        # 获取链接和声音标题
        '''
        第一页:
        https: // www.ximalaya.com / revision / album?albumId = 233686

        ttps: // www.ximalaya.com / revision / album / getTracksList?albumId = 2850165 & pageNum = 4
        #　接口：
        get_url = https://www.ximalaya.com/revision/play/album?albumId=2850165&pageNum=1
        # get :
        # 参数:
        # albumId: 2850165
        # pageNum: 1
        # sort: -1
        # pageSize: 30

        '''
        # 声音
        # get_url = 'https://www.ximalaya.com/revision/album?albumId='+str(albumId)

        # yield scrapy.Request(url=get_url,callback=self.parse_audio,meta={'item':item})
'''
    def parse_audio(self,response):

        item = response.meta['item']
        base_url = response.url
        # 获取接口数据

        audio_lists = response.text['data']['tracksInfo']['tracks']
        for audio in audio_lists:
            try:

                item['title'] = audio['title']
                item['audio_url'] = str(base_url) + audio['url']
            except Exception as e:
                item['title'] = ''
                item['audio_url'] = ''
'''
