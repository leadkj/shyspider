import scrapy
from scrapy_redis.spiders import RedisSpider
from MySpider.items import PicurlItem, BeautyItem
from MySpider.spiders import ua

class PicsSpider(RedisSpider):
    name = 'pics'
    allowed_domains = ['taotuxp.com']
    # start_urls = ["https://www.taotuxp.com/251131.html"]

    custom_settings = {
        "ITEM_PIPELINES": {
            'MySpider.pipelines.SubBeautyRedisPipeline': 200,
            'MySpider.pipelines.SubBeautyPipeline': 200,
        },
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Referer': "https://www.taotuxp.com/xiuren",
            'User-Agent': ua.random
        }
    }

    def parse(self, response):
        print(response.url)
        beauty = response.url.split("/")[3].rstrip(".html")
        beauty_name = response.xpath("//h1/text()").get()
        category = response.xpath("//a[@rel='category tag']/@href").get().split("/")[-1]
        sub_beauty = response.xpath("//div[@class='pagelist']/a")
        for pic in sub_beauty:
            item = BeautyItem()
            url = pic.xpath("./@href").get()
            beauty = beauty
            beauty_name = beauty_name
            category = category
            print(url, beauty, beauty_name, category)
            item['beauty_name'] = beauty_name
            item['url'] = url
            item['category'] = category
            item['beauty'] = beauty
            yield item
