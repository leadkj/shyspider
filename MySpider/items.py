# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    search_num = scrapy.Field()

#url ,beauty,beauty_name
class ImgsrcItem(scrapy.Item):
    beauty_name = scrapy.Field()
    beauty = scrapy.Field()
    url = scrapy.Field()


class CategoryItem(scrapy.Item):
    category_name = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()


class BeautyItem(scrapy.Item):
    beauty_name = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    beauty = scrapy.Field()


class PicurlItem(scrapy.Item):
    url = scrapy.Field()
    beauty = scrapy.Field()
