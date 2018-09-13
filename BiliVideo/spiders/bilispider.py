# -*- coding: utf-8 -*-
import scrapy
from BiliVideo.items import TypeItem,VideoItem


class BilispiderSpider(scrapy.Spider):
    name = 'bilispider'
    start_urls = ['https://bilibili.com/ranking']
    def parse(self, response):
        types=response.xpath('//*[@id="primary_menu"]/ul/li/a/div[2]/text()').extract()
        subtypes=[]
        suburls=[]
        for i in range(2,len(types)+2):
            suburls.append(response.xpath('//*[@id="primary_menu"]/ul/li[{}]/ul/li/a/@href'.format(i)).extract())
            subtypes.append(response.xpath('//*[@id="primary_menu"]/ul/li[{}]/ul/li/a/span/text()'.format(i)).extract())
        for type,subtype,suburl in zip(types,subtypes,suburls):
            for j,k in zip(subtype,suburl):
                item=TypeItem()
                item['type']=type
                item['subtype']=j
                item['subtype_url']=k.replace('//','')
                yield scrapy.http.Request(url="https://"+item['subtype_url'],callback=self.parse_item)
        # self.request_url(suburls)
    def request_url(self,urls):
        for url in urls:
            if type(url) is list:
                self.request_url(url)
            yield scrapy.http.Request(url=url,callback=self.parse_item)
            # print(url)
    def parse_item(self, response):
        print(response.text)
        video_urls=response.xpath('//*[@id="videolist_box"]/div[2]/ul/li/div/div[2]/a/@href').extract()
        titles=response.xpath('//*[@id="videolist_box"]/div[2]/ul/li/div/div[2]/a/text()').extract()
        watched_times=response.xpath('//*[@id="videolist_box"]/div[2]/ul/li/div/div[2]/div[2]/span[1]/span/text()').extract()
        up_authors=response.xpath('//*[@id="videolist_box"]/div[2]/ul/li/div/div[2]/div[3]/a/text()').extract()
        danmu_barrages=response.xpath('//*[@id="videolist_box"]/div[2]/ul/li/div/div[2]/div[2]/span[1]/span/text()').extract()
        for video_url,title,watched_time,up_author,danmu_barrage in zip(
                video_urls,titles,watched_times,up_authors,danmu_barrages):
            item = VideoItem()
            item['video_url']=video_url.replace('//','')
            item['title']=title
            item['watched_time']=watched_time
            item['up_author']=up_author
            item['danmu_barrage']=danmu_barrage
            yield item
