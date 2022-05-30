from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from LeroyParse import settings
from LeroyParse.spiders.Leroy import LeroySpider


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    search = 'wallpaper'
    process.crawl(LeroySpider, search=search)
    process.start()
