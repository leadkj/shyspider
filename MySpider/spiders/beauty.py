import scrapy
import json
from MySpider.spiders import ua
from MySpider.items import BeautyItem


class BeautySpider(scrapy.Spider):
    name = 'beauty'
    allowed_domains = ['taotuxp.com']
    start_urls = []
    with open('../data/category.json', 'r') as f:
        for line in f.readlines():
            if line.strip():
                url = json.loads(line)['url']
                if url.startswith("https"):
                    start_urls.append(url)

    custom_settings = {
        "ITEM_PIPELINES": {
            'MySpider.pipelines.BeautyPipeline': 200,
        },
        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Referer': "https://www.taotuxp.com/xiuren",
            'User-Agent': ua.random
        }
    }

    def parse(self, response):
        beautys = response.xpath("//ul[@id='post_container']/li")
        for beauty in beautys:
            item = BeautyItem()
            beauty_name = beauty.xpath("./div[@class='article']/h2/a/text()").get()
            url = beauty.xpath("./div[@class='article']/h2/a/@href").get()
            category = \
            beauty.xpath("./div[@class='info']/span[@class='info_category info_ico']/a/@href").get().split("/")[3]
            beauty = url.split("/")[3].split('.')[0]
            item['beauty_name'] = beauty_name
            item['url'] = url
            item['category'] = category
            item['beauty'] = beauty

            yield item
        next = response.xpath("//a[contains(@class,'next')]/@href").get()
        if next:
            url = response.urljoin(next)
            yield scrapy.Request(url=url, callback=self.parse)
