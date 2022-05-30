import scrapy
from scrapy.http import HtmlResponse
from LeroyParse.items import LeroyparseItem
from scrapy.loader import ItemLoader
from pprint import pprint



class LeroySpider(scrapy.Spider):
    name = 'Leroy'
    allowed_domains = ['castorama.ru']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://www.castorama.ru/decoration/{kwargs.get("search")}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[contains(@class,'toolbar-bottom')]//a[contains(@class,'i-next')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[contains(@class, "product-card__name")]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.product_parse)



    def product_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparseItem(), response=response)
        loader.add_xpath('_id', '//span[@itemprop="sku"]/text()')
        loader.add_xpath('name', '//h1[contains(@class,"product-essential__name")]/text()')
        loader.add_xpath('price',
                         '//div[contains(@class, "add-to-cart__price")]//span[@class="price"]/span/span[1]/text()')
        loader.add_xpath('currency',
                         '//div[contains(@class, "add-to-cart__price")]//span[@class="currency"]/text()')
        loader.add_value('link', response.url)
        loader.add_xpath('photos',
                         '//div[@class="js-zoom-container"]/img[contains(@src, "https://www.castorama.ru/")]/@src | '
                         '//div[@class="js-zoom-container"]/img[contains(@data-src, "https://www.castorama.ru/")]/@data-src')

        character_key = response.xpath('//div[contains(@class,"product-specifications")]/dl/dt/span/text()').getall()
        character_value = response.xpath('//div[contains(@class,"product-specifications")]/dl/dd/text()').getall()
        characteristics = dict(zip(character_key, character_value))
        loader.add_value('characteristics', characteristics)

        yield loader.load_item()


        # name = response.xpath('//h1[@itemprop="name"]/text()')
        # price = response.xpath('//span[@slot="price"]')
        # currency = response.xpath("//span[@slot='currency']")
        # url = response.url
