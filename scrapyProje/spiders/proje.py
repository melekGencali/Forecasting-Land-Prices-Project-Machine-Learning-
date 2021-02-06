# -*- coding: utf-8 -*-
import scrapy
from scrapyProje.items import ScrapyprojeItem

class ProjeSpider(scrapy.Spider):
    name = 'proje'
    allowed_domains = ['hurriyetemlak.com']
    start_urls = [
                 'https://www.hurriyetemlak.com/satilik/arsa?page=1100' ]

    def parse(self, response):
        print('Page URL: ' + response.url)

        for url in response.css('div.list-view-img-wrapper>a::attr(href)').getall():

            print('requesting: ' + url)
            yield scrapy.Request('https://www.hurriyetemlak.com'+url, callback=self.parseData)

    def parseData(self, response):

       item = ScrapyprojeItem()
       features = {}

       item["fiyat"]=response.css('p::text').extract()[0].strip()
       item["il"]=response.css('ul.short-info-list>li::text').extract()[0].strip()
       item["ilce"]=response.css('ul.short-info-list>li::text').extract()[1].strip()
       item["mahalle"]=response.css('ul.short-info-list>li::text').extract()[2].strip()

       for feature in response.css('ul.adv-info-list>li'):
         # for feature in response.css('li.col-md-6'):
         key = feature.css('span.txt::text').extract()[0]
         value = feature.css('span::text').extract()[1]
         # field adı : içeriği yan yana yazılması için aşağıdaki eşitleme yazılır.
         features[key.strip()] = value.strip()
         if features is not None:
             item['features'] = features
       yield item



