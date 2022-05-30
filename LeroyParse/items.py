# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from typing import Union

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def process_price(raw_price: list) -> Union[float, list]:
    try:
        price = '.'.join(raw_price).replace(' ', '')
        return float(price)
    except Exception:
        return raw_price


def process_characteristics(raw_dict: {}) -> {}:
    char_dict = raw_dict[0]
    try:
        for k, v in char_dict.items():
            v = v.replace('\n', '').strip()
            char_dict[k] = v
    except Exception:
        pass
    return char_dict


def process__id(raw__id: list) -> int:
    try:
        _id = int(raw__id[0])
        return _id
    except Exception:
        return raw__id


class LeroyparseItem(scrapy.Item):
    _id = scrapy.Field(input_processor=Compose(process__id), output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    characteristics = scrapy.Field(input_processor=Compose(process_characteristics), output_processor=TakeFirst())

