# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        school_id = (spider.name, item['school_id'])
        if school_id in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(school_id)
            return item

class ApplySpiderNamePipeline(object):

    def process_item(self, item, spider):
        existing_extras = item.get('extras', {})
        existing_extras['@spider'] = spider.name
        item['extras'] = existing_extras

        return item
