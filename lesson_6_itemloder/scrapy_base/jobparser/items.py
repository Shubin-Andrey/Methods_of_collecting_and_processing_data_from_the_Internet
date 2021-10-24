import scrapy
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Identity
from w3lib.html import remove_tags


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    pass


class LeruaparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field(
   )
    description = scrapy.Field(
   )
    photos = scrapy.Field(
   )
    price = scrapy.Field(
   )
    price_curr = scrapy.Field(
   )
    specifications = scrapy.Field(
   )
    url_rs = scrapy.Field(
   )
    pass
