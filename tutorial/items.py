# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst

def remove_quotes(text):
    # strip the unicode quotes
    text = text.strip('\"')
    return text


class QuoteItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    quote_content  = Field()