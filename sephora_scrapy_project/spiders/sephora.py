# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


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

    def parse_item(self, response):

        brand_name = response.xpath(
            "//h1[@data-comp='DisplayName Flex Box']" +
            "//span[@class='css-euydo4']//text()"
        ).extract_first()

        item_name = response.xpath(
            "//h1[@data-comp='DisplayName Flex Box']" +
            "//span[@class='css-0']//text()"
        ).extract_first()

        price = response.xpath(
            "//div[@data-comp='Price Box']//text()"
        ).extract_first()

        ingredient = response.xpath(
            "//div[@data-at='product_tabs_section']" +
            "//div[@id='tabpanel2']" +
            "//div[@class='css-pz80c5']//text()"
        ).extract_first()

        yield {
            "brand_name": brand_name,
            "item_name": item_name,
            "price": price,
            "ingredient": ingredient
        }
