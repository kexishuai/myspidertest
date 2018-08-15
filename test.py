import re

import requests
from lxml import html

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}
def gen_url(url):
    response = requests.get(url=url,headers=headers,verify=False)
    ret = re.compile(r'//item.jd.com/(\d+).html')
    id_list = ret.findall(response.text)
    for id in id_list:
        detail_url = 'https://item.jd.com/'+str(id)+'.html'
        parse_detail(detail_url)
def parse_detail(detail_url):
    response = requests.get(url=detail_url,headers=headers,verify=False)

    element = html.etree.HTML(response.text)

    price = element.xpath('//span[@class="p-price"]')[0].text
    title = element.xpath('//div[@class="sku-name"]')[0].text
    print(title)

url = 'https://list.jd.com/list.html?cat=9987,653,655'
gen_url(url)
