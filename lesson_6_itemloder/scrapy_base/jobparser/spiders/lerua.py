import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
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
        l = ItemLoader(item=LeruaparserItem(), response=response)
        specifications = {}
        specifications_1 = response.xpath('//*[@id="nav-characteristics"]/uc-pdp-section-layout/uc-pdp-section-vlimited/dl/div[@class ="def-list__group"]/dt//text()').extract()
        specifications_2 = response.xpath('//*[@id="nav-characteristics"]/uc-pdp-section-layout/uc-pdp-section-vlimited/dl/div[@class ="def-list__group"]/dd//text()').extract()
        for i, el in enumerate(specifications_1):
            specifications[el] = ''.join(specifications_2[i].split())
        url_rs = response.url

        l.add_xpath("name", '//h1[@class="header-2"]//text()')
        l.add_xpath("description", '//section[@class="pdp-section pdp-section--product-description"]//text()')
        l.add_xpath("photos", '//img[contains(@alt, "product image")]/@src')
        l.add_xpath("price", '//span[@slot="price"]//text()')
        l.add_xpath("price_curr", '//span[@slot="currency"]//text()')
        l.add_value("specifications", specifications)
        l.add_value("url_rs", url_rs)
        print('Идет процесс')

        yield l.load_item()


