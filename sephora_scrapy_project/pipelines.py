# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import logging
import boto3
from botocore.exceptions import ClientError

from scrapy import signals
from scrapy.exporters import CsvItemExporter
import datetime

PROJECT_S3_BUCKET_NAME = "sephora-scraped-data"


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True


class CsvExportorPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        today = datetime.date.today()
        self.file_name = '%(spider_name)s_%(date_time)s.csv' % {
            'spider_name': spider.name,
            'date_time': today
        }
        self.file = open(self.file_name, 'w+b')
        self.exporter = CsvItemExporter(self.file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
        if not upload_file(self.file_name, PROJECT_S3_BUCKET_NAME):
            raise Exception("Fail to upload result to s3 bucket")
        logging.info("Uploaded result to S3")
        #if os.path.exists(self.file_name):
        #    os.remove(self.file_name)

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
