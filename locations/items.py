# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# class AddressItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class AddressItem(scrapy.Item):
    # define the fields for your item here:

    school_id = scrapy.Field()
    name = scrapy.Field()
    street_address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    postcode = scrapy.Field()
    ref = scrapy.Field()
    website = scrapy.Field()
    extras = scrapy.Field()
