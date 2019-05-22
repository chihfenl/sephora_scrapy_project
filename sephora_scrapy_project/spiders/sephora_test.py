# -*- coding: utf-8 -*-
import sys
import os

from six.moves.urllib.parse import urljoin
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.utils.python import to_native_str
from sephora_scrapy_project.items import SephoraScrapyProjectItem

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from libs.sephora_next_link_extractor import SephoraNextLinkExtractor


class SephoraTestSpider(CrawlSpider):
    name = 'sephora_test'
    allowed_domains = ['sephora.com']
    start_urls = ['http://www.sephora.com/brand/clinique/all']
    handle_httpstatus_list = [301, 302]

    rules = [
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

        yield loader.load_item()
