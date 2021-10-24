from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser.spiders.lerua import LeruaSpider
from jobparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaSpider, mark='мебель')
    process.start()
