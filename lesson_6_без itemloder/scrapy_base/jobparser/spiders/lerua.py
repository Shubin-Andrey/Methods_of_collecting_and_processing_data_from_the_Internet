import scrapy
import json
from scrapy.http import HtmlResponse

from jobparser.items import LeruaparserItem


class LeruaSpider(scrapy.Spider):
    name = 'lerua'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, mark):
        self.start_urls = [f'https://leroymerlin.ru/search/?q={mark}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//div[@class="phytpj4_plp largeCard"]//a[@class="bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp"]'
                                   '//@href').extract()
        for link in ads_links:
            yield response.follow('https://leroymerlin.ru' + link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        specifications = {}
        name = response.xpath('//h1[@class="header-2"]//text()').extract()
        description = response.xpath('//section[@class="pdp-section pdp-section--product-description"]//text()').extract()
        photos = response.xpath('//img[contains(@alt, "product image")]/@src').extract()
        price = response.xpath('//span[@slot="price"]//text()').getall()
        price_curr = response.xpath('//span[@slot="currency"]//text()').getall()
        specifications_1 = response.xpath('//*[@id="nav-characteristics"]/uc-pdp-section-layout/uc-pdp-section-vlimited/dl/div[@class ="def-list__group"]/dt//text()').extract()
        specifications_2 = response.xpath('//*[@id="nav-characteristics"]/uc-pdp-section-layout/uc-pdp-section-vlimited/dl/div[@class ="def-list__group"]/dd//text()').extract()
        for i, el in enumerate(specifications_1):
            specifications[el] = ''.join(specifications_2[i].split())
        url_rs = response.url
        print(name[0], price, url_rs, specifications)
        print(photos)

        yield LeruaparserItem(name=name, description=description, photos=photos, price=price, price_curr=price_curr, specifications=specifications, url=url_rs)


