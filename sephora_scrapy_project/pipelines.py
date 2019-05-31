# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import signals
from scrapy.exporters import CsvItemExporter
import datetime

DATASTORE_ROOT_DIR = './data'


class CsvExportorPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        today = datetime.date.today()
        file_name = '%(spider_name)s_%(date_time)s.csv' % {
            'spider_name': spider.name,
            'date_time': today
        }
        file_name = '/'.join([DATASTORE_ROOT_DIR, file_name])
        self.file = open(file_name, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
