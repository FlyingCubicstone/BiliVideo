# -*- coding: utf-8 -*-
import scrapy
from BiliVideo.items import VideoItem

class SubspiderSpider(scrapy.Spider):
    name = 'subspider'
    allowed_domains = ['bilibili.com']
    start_urls = ['https://www.bilibili.com/v/anime/offical#']

    def parse(self, response):
        item = VideoItem()
        print('===================', response.text)
        # item['image']=response.xpath('//*[@id="videolist_box"]/div[2]/ul/li/div/div[1]/div/a/div/div[1]/img/@src').extract()
        # item['image']=response.xpath('//*[@class="lazy-img"]/@src').extract()
        item['title']=response.xpath('//*[@id="videolist_box"]/div[2]/ul/li')
        # item['title'] = response.xpath('/html/head/title/text()').extract()
        # item['up_author']=response.xpath('//*[@id="videolist_box"]/div[2]/ul/li')
        # item['watched_time']=response.xpath('//*[@id="videolist_box"]/div[2]/ul/li')
        # item['danmu_barrage']=response.xpath('//*[@id="videolist_box"]/div[2]/ul/li')
        return item
