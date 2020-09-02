import scrapy
from scrapy_redis.spiders import  RedisSpider
import re
from MySpider.items import ImgsrcItem

class ImgsrcSpider(RedisSpider):
    name = 'imgsrc'
    allowed_domains = ['taotuxp.com']
    #start_urls = ['http://taotuxp.com/']

    custom_settings = {
        "ITEM_PIPELINES": {
            #'MySpider.pipelines.BeautyDownloadPipeline': 200,
            'MySpider.pipelines.BeautyDownloadMysqlPipeline':200,
            #'MySpider.pipelines.SaveImagePipeline': 200,
        },
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Referer': "https://www.taotuxp.com/xiuren",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
    }


    def parse(self, response):
        beauty_name = response.xpath("//h1/text()").get()
        beauty = re.findall(r'/(\d+).html',response.url)[0]
        imgs = response.xpath("//div[@id='post_content']/p")
        for img in imgs:
            item = ImgsrcItem()
            imgsrc = img.xpath("./img/@src").get()
            item['beauty_name'] = beauty_name
            item['beauty'] = beauty
            item['url'] = imgsrc
            yield item

