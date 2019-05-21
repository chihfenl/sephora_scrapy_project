# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from sephora_scrapy_project.items import SephoraScrapyProjectItem


class SephoraTestSpider(scrapy.Spider):
    name = 'sephora_test'

    def start_requests(self):
        start_urls = ['https://www.sephora.com/brand/clinique/all']
        return [scrapy.Request(url=url, callback=self.parse_item)
                for url in start_urls]

    def parse_item(self, response):

        for url in response.xpath(
            "//div[@class='css-dkxsdo']" +
            "//div[@class='css-12egk0t']" +
            "//a[@class='css-ix8km1']//@href"
        ).extract():
            yield {'url': url}
