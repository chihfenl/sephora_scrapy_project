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

        item_name = response.xpath(
            "//span[@class='css-0']//text()"
        ).extract_first()
        yield {
            "item_name": item_name
        }
