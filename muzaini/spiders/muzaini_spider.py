import scrapy
from scrapy.spider import BaseSpider
from scrapy.utils.response import open_in_browser
from scrapy.shell import inspect_response
from scrapy.selector import Selector
from muzaini.items import MuzainiItem
import datetime

class MuzainiSpider(BaseSpider):
    name = "muzaini"
    allowed_domains = ["muzaini.com"]

    def start_requests(self):
        urls = [
            'http://www.muzaini.com/ExchangeRates.aspx'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
  
    def parse (self,response):
        sel = Selector(response)
        item = MuzainiItem()
        #open_in_browser(response)
        #inspect_response(response)
        
        item['base_currency'] = response.xpath('//*[@id="ddlCurrency"]/option[1]/text()').extract()[0]
 
        for tr in sel.xpath('//div[@id="UpdatePanel1"]/table/tbody/tr'):
            item['currency'] = tr.xpath('./td[1]/text()').extract()[0].strip()
            item['buy'] = tr.xpath('./td//div[@class="fcbuyrate"]/text()').extract()[0]
            item['sell'] = tr.xpath('./td//div[@class="fcsellrate"]/text()').extract()[0]
            item['date'] = datetime.datetime.now()
            
            yield item
            
        #try:
        #    yield item
        #except Error:
        #    print "parse exception"