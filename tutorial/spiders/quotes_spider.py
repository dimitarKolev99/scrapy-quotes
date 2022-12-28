import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem

class QutoesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote, response=response)
            loader.add_css('quote_content', '.text::text')
            yield loader.load_item()