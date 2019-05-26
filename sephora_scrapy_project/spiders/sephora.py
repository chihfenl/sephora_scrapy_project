# -*- coding: utf-8 -*-
import os
import sys

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from sephora_scrapy_project.items import SephoraScrapyProjectItem

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from libs.sephora_next_link_extractor import SephoraNextLinkExtractor


class SephoraSpider(CrawlSpider):
    name = 'sephora'
    allowed_domains = ['sephora.com']
    start_urls = ['http://www.sephora.com/brands-list']

    rules = [
        Rule(
            LinkExtractor(
                allow=".*",
                restrict_xpaths="//li[@class='css-1hhsxaa ']/a",
            ),
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=".*",
                restrict_xpaths="//div[@class='css-1hnm2t1 ']" +
                                "//a[contains(@href, 'all')]",
            ),
            follow=True
        ),
        Rule(SephoraNextLinkExtractor(), follow=True),
        Rule(
            LinkExtractor(
                allow=".*",
                restrict_xpaths="//div[@class='css-12egk0t']" +
                                "//a[@class='css-ix8km1']",
            ),
            follow=True,
            callback='parse_item'
        )
    ]

    def _get_detail_and_ingredient_column_num(self, response):

        index = 0
        detail_col_num = None
        ingredient_col_num = None

        for tab_name in response.xpath(
            "//div[@data-at='product_tabs_section']" +
            "//div[@role='tablist']//button//text()"
        ).extract():

            if tab_name == 'Details':
                detail_col_num = str(index)
            if tab_name == 'Ingredients':
                ingredient_col_num = str(index)
            index += 1

        return (detail_col_num, ingredient_col_num)

    def parse_item(self, response):

        loader = ItemLoader(item=SephoraScrapyProjectItem(), response=response)

        loader.add_xpath(
            'brand_name',
            "//h1[@data-comp='DisplayName Flex Box']" +
            "//span[@class='css-euydo4']//text()"
        )

        loader.add_xpath(
            'item_name',
            "//h1[@data-comp='DisplayName Flex Box']" +
            "//span[@class='css-0']//text()"
        )

        loader.add_xpath(
            'price',
            "//div[@data-comp='Price Box']//text()"
        )

        detail_col_num, ingredient_col_num = \
            self._get_detail_and_ingredient_column_num(response)

        if detail_col_num:
            tabpanel_number = ''.join(['tabpanel', detail_col_num])
            xpath_str = \
                "//div[@data-at='product_tabs_section']" + \
                "//div[@id='{}']".format(tabpanel_number) + \
                "//div[@class='css-pz80c5']//text()"
            loader.add_xpath('details', xpath_str)

        if ingredient_col_num:
            tabpanel_number = ''.join(['tabpanel', ingredient_col_num])
            xpath_str = \
                "//div[@data-at='product_tabs_section']" + \
                "//div[@id='{}']".format(tabpanel_number) + \
                "//div[@class='css-pz80c5']//text()"
            loader.add_xpath('ingredient', xpath_str)

        return loader.load_item()
