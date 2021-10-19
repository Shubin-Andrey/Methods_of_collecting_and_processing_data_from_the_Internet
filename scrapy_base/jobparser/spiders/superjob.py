# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=ML&geo%5Bt%5D%5B0%5D=4']


    def parse(self, response: HtmlResponse):
        next_page = 'https://www.superjob.ru' \
                    + response.css('a[rel="next"]').attrib['href']
        print(next_page)
        response.follow(next_page, callback=self.parse)
        vacansy = response.css(
            'div.[class="f-test-search-result-item"]'
        ).extract()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('[class^="icMQ_"]').getall()
        firm_name = response.css('[class^="_1h3Zg _3Fsn4"]').getall()
        salary = ' '.join(response.css('[class^="_1OuF_"]')).getall()
        work_href = response.css('[class^="icMQ_"]').attrib['href']
        #print('\nНазвание вакансии: ', name[0])
        #('Зарплата: ', salary, '****', salary_from)
        #print(work_href)
        yield JobparserItem(name=name, firm_name=firm_name, salary=salary, work_href=work_href)
