# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy.spiders import Rule

# from scrapy.spiders import CrawlSpider  #链接提取
from scrapy_redis.spiders import CrawlSpider # 分布式爬取
from scrapy.linkextractors import LinkExtractor
import pprint

class JdSpider(CrawlSpider):
    name = 'jd-redis'
    allowed_domains = ['jd.com','p.3.cn']
    start_urls = ['https://m.jd.com/']

    rules = {
        Rule(LinkExtractor(allow=()),
             callback='parse_detail',
             follow=True),
    }

    # custom_settings = {
    #
    #     'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
    #     'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
    #     'SCHEDULER_PERSIST': True,
    #     'ITEM_PIPELINES': {
    #         'scrapy_redis.pipelines.RedisPipeline': 400,
    #     },
    #     'DOWNLOAD_DELAY': '1',
    #     # 配置redis的地址和端口
    #     # 'REDIS_HOST': '10.36.132.227',
    #     'REDIS_HOST': '127.0.0.1',
    #     'REDIS_PORT': '6379',
    # }

    def parse_detail(self,response):

        ware_id_list = []
        url_group_shop = LinkExtractor(allow=(r'(https|http)://item.m.jd.com/product/\d+.html')).extract_links(response)
        re_get_id = re.compile(r'(https|http)://item.m.jd.com/product/(\d+).html')
        for url in url_group_shop:
            ware_id = re_get_id.search(url.url).group(2)
            ware_id_list.append(ware_id)
        '''
        https://item.m.jd.com/ware/detail.json?wareId={}  详情
        https://p.3.cn/prices/mgets?type=1&skuIds=J_{}   价格
        '''
        for id in ware_id_list:
            yield scrapy.Request('https://item.m.jd.com/ware/detail.json?wareId={}'.format(id),
                                 callback=self.detail_pag,
                                 meta={'id':id},
                                 priority=5)

    def detail_pag(self,response):
        _ = self
        data = json.loads(response.text)

        yield scrapy.Request('https://p.3.cn/prices/mgets?type=1&skuIds=J_{}'.format(response.meta['id']),
                             callback=self.get_price_pag,
                             meta={'id': response.meta['id'],
                                   'data':data},
                             priority=10
                             )
    def get_price_pag(self,response):
        _ = self
        data = json.loads(response.text)
        detail_data = response.meta['data']
        ware_id = response.meta['id']
        item = {
            'detail':detail_data,
            'price':data,
            'ware_id':ware_id

        }
        print(item)
        pprint.pprint(item)
        yield item