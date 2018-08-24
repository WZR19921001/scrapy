# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem

class DemoSpider(scrapy.Spider):
    name = 'demo'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']
    #默认解析方法
    def parse(self, response):
        #循环电影的条目
        move_list = response.xpath("//div[@class='article']/ol[@class='grid_view']/li")
        for i in move_list:
            douban_item = DoubanItem()
            douban_item['number'] = i.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['move_name'] = i.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()
            strings = i.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            #介绍为多行字符串 需要切割 拼接
            for j in strings:
                string = "".join(j.split())
                douban_item["introduce"] = string

            douban_item["star"] = i.xpath(".//span[@class= 'rating_num']/text()").extract_first()
            douban_item["evaluate"] = i.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            douban_item["describe"] = i.xpath(".//p[@class='quote']/span/text()").extract_first()

            yield douban_item

        #解析下一页规则，取得后页的xpath
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)