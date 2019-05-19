# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from sephora_scrapy_project.items import SephoraScrapyProjectItem


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

    def _get_ingredient_order(self, response):

        index = 0

        for tab in response.xpath(
            "//div[@data-at='product_tabs_section']" +
            "//div[@role='tablist']//button//text()"
        ).extract():

            if tab == 'Ingredients':
                return str(index)
            index += 1

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

        ingredient_order = self._get_ingredient_order(response)

        if ingredient_order:
            tabpanel_number = ''.join(['tabpanel', ingredient_order])
            xpath_str = \
                "//div[@data-at='product_tabs_section']" + \
                "//div[@id='{}']".format(tabpanel_number) + \
                "//div[@class='css-pz80c5']//text()"
            loader.add_xpath('ingredient', xpath_str)

        return loader.load_item()
