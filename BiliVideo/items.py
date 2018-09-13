# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class TypeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    collection='type'
    type=scrapy.Field()
    subtype=scrapy.Field()
    subtype_url=scrapy.Field()
class VideoItem(scrapy.Item):
    collection='video'
    video_url=scrapy.Field()
    title=scrapy.Field()
    up_author=scrapy.Field()
    watched_time=scrapy.Field()
    danmu_barrage=scrapy.Field()
