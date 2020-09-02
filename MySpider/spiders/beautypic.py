import scrapy
from MySpider.items import CategoryItem
from MySpider.spiders import ua


class BeautypicSpider(scrapy.Spider):
    name = 'beautypic'
    allowed_domains = ['taotuxp.com']
    start_urls = ['https://www.taotuxp.com/']

    custom_settings = {
        "ITEM_PIPELINES": {
            'MySpider.pipelines.CategoryPipeline': 200,
        },
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Referer': "https://www.taotuxp.com/xiuren",
            'User-Agent': ua.random
        }
    }

    def parse(self, response):
        categorys = response.xpath('//ul[@id="menu-taotucd"]/li')
        for category in categorys:
            item = CategoryItem()
            category_name = category.xpath("./a/text()").get()
            url = category.xpath("./a/@href").get()
            category = url.split("/")[3]
            item['category_name'] = category_name
            item['url'] = url
            item['category'] = category
            yield item
