import scrapy
from MySpider.spiders import ua
from MySpider.items import MyspiderItem


class BaidunewsSpider(scrapy.Spider):
    name = 'baidunews'
    allowed_domains = ['baidu.com']
    start_urls = ['http://top.baidu.com/?fr=mhd_card']

    custom_settings = {
        "ITEM_PIPELINES": {
            'MySpider.pipelines.MyspiderPipeline': 300,
            'MySpider.pipelines.CustomPipeline': 200,
        },
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Referer': "https://www.baidu.com",
            'User-Agent': ua.random
        }
    }

    def parse(self, response):
        new_list = response.xpath("//ul[@id='hot-list']/li")
        for new in new_list:
            item = MyspiderItem()
            title = new.xpath("./a/@title").get()
            url = new.xpath("./a/@href").get()
            search_num = new.xpath("./span[contains(@class,'icon-')]/text()").get()  # 每次访问class 都变化，icon- 后面的不确定
            item['title'] = title
            item['url'] = url
            item['search_num'] = search_num
            yield item
