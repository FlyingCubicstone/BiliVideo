# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from scrapy import signals

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
import logging

class BilivideoSpiderMiddleware(object):
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


class BilivideoDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self,service_args=[]):
        self.timeout=20
        # self.browser=webdriver.PhantomJS(service_args=service_args)
        self.browser=webdriver.Chrome()
        self.browser.set_page_load_timeout(self.timeout)
        self.wait=WebDriverWait(self.browser,self.timeout)
        self.logger=logging.getLogger(__name__)

    def __del__(self):
        self.browser.quit()

    def process_request(self,request,spider):
        self.logger.debug("+++++")
        self.logger.debug(request.url)
        self.logger.debug("+++++")
        try:
            self.browser.get(request.url)
            if request.url not in ['https://bilibili.com','http://bilibili.com',
                               'https://www.bilibili.com','http://www.bilibili.com',
                               'https://bilibili.com/ranking','http://bilibili.com/ranking',
                               'https://www.bilibili.com/ranking', 'http://www.bilibili.com/ranking',]:
                next=self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,'#videolist_box > div.vd-list-cnt > div.pager.pagination'+
                                     '> ul > li.page-item.next > button')))
                # videolist_box > div.vd-list-cnt > div.pager.pagination > ul > li.page-item.next > button
                # videolist_box > div.vd-list-cnt > div.pager.pagination > ul > li.page-item.next > button
                time.sleep(1)
                next.click()
            return HtmlResponse(url=request.url, body=self.browser.page_source,
                                request=request, encoding='utf-8', status=200)
        except TimeoutException:
            return HtmlResponse(url=request.url,status=500,request=request)

    @classmethod
    def from_crawler(cls,crawler):
        return cls(service_args=crawler.settings.get('PHANTOMJS_SERVICE_ARGS'))