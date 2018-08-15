# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from scrapy_redis.spiders import RedisCrawlSpider

class ToredisSpider(RedisCrawlSpider):
    name = 'Toredis'
    allowed_domains = ['www.ximalaya.com']

    redis_key = 'toredisspider:start_urls'
    page_link = LinkExtractor(allow=r'https://www.ximalaya.com/youshengshu/p\d+')

    # detail_link = LinkExtractor(restrict_xpaths='//div[@class="movie-item-in"]/a')

    rules = (
        Rule(page_link, follow=True),
        #Rule(detail_link, callback='parse_detail', follow=False)
    )


    custom_settings = {

        'DUPEFILTER_CLASS': "scrapy_redis.dupefilter.RFPDupeFilter",
        'SCHEDULER': "scrapy_redis.scheduler.Scheduler",
        'SCHEDULER_PERSIST': True,
        'ITEM_PIPELINES': {
            'scrapy_redis.pipelines.RedisPipeline': 400,
        },
        'DOWNLOAD_DELAY': '1',
        # 配置redis的地址和端口
        # 'REDIS_HOST': '10.36.132.227',
        'REDIS_HOST': '127.0.0.1',
        'REDIS_PORT': '6379',
    }

    def parse(self, response):
        li_list = response.xpath('//div[@class="content"]/ul/li')
        for li in li_list:
            item = {}
            img_url = li.xpath('./div/div/a/img/@src').extract()[0]
            book_name = li.xpath('./div/a')[0].xpath('string(.)').extract()[0]
            book_author = li.xpath('./div/a')[1].xpath('string(.)').extract()[0][3:]
            detail_url = 'https://www.ximalaya.com' + li.xpath('./div/a')[0].xpath('./@href').extract()[0]
            item['img_url'] = img_url
            item['book_name']= book_name
            item['book_author'] = book_author
            item['detail_url'] = detail_url
            yield item
