# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import time
import logging

from scrapy import signals
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver.chrome.options import Options

TOTAL_ITEM_GROUPS = 5


class ChromeWebDriver(object):

    def __init__(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=options)

    def _scroll_page_down(self):
        total_groups_str = str(TOTAL_ITEM_GROUPS)
        for group_num in range(0, TOTAL_ITEM_GROUPS):
            self.driver.execute_script(
                """
                window.scrollTo(
                document.body.scrollHeight*{}/{},
                document.body.scrollHeight*{}/{}
                );
                """
                .format(
                    str(group_num), total_groups_str,
                    str(group_num + 1), total_groups_str
                )
            )
            time.sleep(50.0 / 1000.0)

    def safe_get_full_page_body(self, page_url):
        self.driver.get(page_url)
        self._scroll_page_down()
        return self.driver.page_source.encode('utf-8')

    def close_driver(self):
        if self.driver:
            self.driver.quit()


class SephoraScrapyProjectSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SephoraScrapyProjectDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    @classmethod
    def process_request(cls, request, spider):
        if '/all' in request.url or '/product' in request.url:
            LOGGER.setLevel(logging.WARNING)
            chrome_webdriver = ChromeWebDriver()
            body = chrome_webdriver.safe_get_full_page_body(request.url)
            chrome_webdriver.close_driver()
            return HtmlResponse(
                request.url, encoding='utf-8', body=body, request=request)

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
