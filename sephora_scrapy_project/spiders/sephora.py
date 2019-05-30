# -*- coding: utf-8 -*-
import os
import sys
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
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

    def get_detail_and_ingredient_column_num(self, response, col_name):

        index = 0
        col_num = None

        for tab_name in response.xpath(
            "//div[@data-at='product_tabs_section']" +
            "//div[@role='tablist']//button//text()"
        ).extract():

            if tab_name == col_name:
                col_num = str(index)
            index += 1

        return col_num

    def get_detail_and_ingredient_xpath(self, response, col_name):

        col_num = self.get_detail_and_ingredient_column_num(response, col_name)

        if not col_num:
            return None

        tabpanel_number = ''.join(['tabpanel', col_num])
        xpath_str = \
            "//div[@data-at='product_tabs_section']" + \
            "//div[@id='{}']".format(tabpanel_number) + \
            "//div[@class='css-pz80c5']//text()"
        return xpath_str

    def get_image_url(self, response):

        image_info = response.xpath(
            "//svg[@class='css-1ixbp0l']//image"
        ).extract_first()
        match_groups = re.search(r'xlink:href=\"(.*?)\"', image_info)
        relative_url = match_groups.group(1)
        absolute_url = response.urljoin(relative_url)

        return absolute_url

    def parse_item(self, response):

        loader = ItemLoader(item=SephoraScrapyProjectItem(), response=response)
        loader.default_output_processor = TakeFirst()

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

        loader.add_xpath(
            'category',
            "//a[@class='css-1ylrown ']//text()"
        )

        loader.add_xpath(
            'subcategory',
            "//a[@class='css-1ylrown ']//text()"
        )

        loader.add_xpath(
            'subsubcategory',
            "//h1[@class='css-bnsadm ']//text()"
        )

        details_xpath = \
            self.get_detail_and_ingredient_xpath(response, 'Details')
        if details_xpath:
            loader.add_xpath('details', details_xpath)

        ingredient_xpath = \
            self.get_detail_and_ingredient_xpath(response, 'Ingredients')
        if ingredient_xpath:
            loader.add_xpath('ingredients', ingredient_xpath)

        image_url = self.get_image_url(response)
        loader.add_value('image_url', image_url)

        return loader.load_item()
