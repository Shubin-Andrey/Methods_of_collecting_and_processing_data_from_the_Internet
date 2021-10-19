import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    salary_from = scrapy.Field()
    salary_to = scrapy.Field()
    salary_currency = scrapy.Field()
    work_href = scrapy.Field()
    site_name = 'HH'

    pass
