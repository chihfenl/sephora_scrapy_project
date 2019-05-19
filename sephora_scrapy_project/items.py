# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SephoraScrapyProjectItem(scrapy.Item):

    brand_name = scrapy.Field()
    item_name = scrapy.Field()
    price = scrapy.Field()
    ingredient = scrapy.Field()
