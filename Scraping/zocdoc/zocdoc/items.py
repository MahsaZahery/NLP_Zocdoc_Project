# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZocdocItem(scrapy.Item):
    doctor = scrapy.Field()
    doctor_type = scrapy.Field()
    text = scrapy.Field()
    name = scrapy.Field()
    num_reviews = scrapy.Field()
    rating = scrapy.Field()