# -*- coding: utf-8 -*-
import sys
import os
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
from sephora_scrapy_project.items import SephoraScrapyProjectItem

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from libs.sephora_next_link_extractor import SephoraNextLinkExtractor


class SephoraTestSpider(CrawlSpider):
    name = 'sephora_test'
    allowed_domains = ['sephora.com']
    start_urls = ['https://www.sephora.com/brand/artis/all']
    handle_httpstatus_list = [301, 302]

    rules = [
        #Rule(SephoraNextLinkExtractor(), follow=True),
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
        loader.default_output_processor = TakeFirst()

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

        image_info = response.xpath(
            "//svg[@class='css-1ixbp0l']//image"
        ).extract_first()
        match_groups = re.search(r'xlink:href=\"(.*?)\"', image_info)
        relative_url = match_groups.group(1)
        absolute_url = response.urljoin(relative_url)

        loader.add_value('image_url', absolute_url)

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
