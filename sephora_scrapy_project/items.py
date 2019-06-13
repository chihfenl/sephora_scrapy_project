# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join, MapCompose
from w3lib.html import remove_tags
from w3lib.html import replace_escape_chars


class SephoraScrapyProjectItem(scrapy.Item):

    brand_name = scrapy.Field()
    item_name = scrapy.Field()
    price = scrapy.Field()
    details = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars),
        output_processor=Join(),
    )
    ingredients = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars),
        output_processor=Join(),
    )
    image_url = scrapy.Field()
    #images = scrapy.Field()
    category = scrapy.Field()
    subcategory = scrapy.Field()
    subsubcategory = scrapy.Field()
