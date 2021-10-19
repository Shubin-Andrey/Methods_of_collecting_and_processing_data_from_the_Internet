# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&text=ML']

    def parse(self, response: HtmlResponse):
        next_page = 'https://izhevsk.hh.ru' \
                    + response.css('a[class="bloko-button"][data-qa="pager-next"]').attrib['href']
        print(next_page)
        response.follow(next_page, callback=self.parse)
        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header '
            'a.bloko-link::attr(href)'
        ).extract()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1[data-qa="vacancy-title"]::text').getall()
        salary = ' '.join(response.css('span[class="bloko-header-section-3 bloko-header-section-3_lite"]::text').getall())
        salary_ = salary.split(' ')
        print(salary_, '************')
        try:
            salary_from = salary_[-5]
            salary_to = salary_[-3]
            salary_currency = salary_[-1]
        except:
            print('нет зп')
        work_href = response.css("a[class='bloko-link'][data-qa='vacancy-serp__vacancy-title']").attrib['href']
        #print('\nНазвание вакансии: ', name[0])
        #('Зарплата: ', salary, '****', salary_from)
        #print(work_href)
        yield JobparserItem(name=name, salary=salary, salary_from=salary_from, salary_to=salary_to, salary_currency=salary_currency,  work_href=work_href)
