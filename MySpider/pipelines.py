# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json,re
import scrapy
import pymysql
from redis import Redis
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

redis_db = Redis(host='db-server',port=6379,db=4)
redis_data_list = "beauty_all_url"

#beauty 分类
class CategoryPipeline:
    def __init__(self):
        self.f = open("category.json","aw")

    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.f.write(content)
        return item

    def close_spider(self,spider):
        self.f.close()
#beauty 连接
class BeautyPipeline:
    def __init__(self):
        self.f = open("beauty.json","w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.f.write(content)
        return item

    def close_spider(self,spider):
        self.f.close()

#子分页连接存入redis
class SubBeautyRedisPipeline:
    def __init__(self):
        pass

    def process_item(self,item,spider):
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        redis_db.lpush(redis_data_list,content)
        return item
    def close_spider(self,spider):
        redis_db.close()
#子分页连接json文件
class SubBeautyPipeline:
    def __init__(self):
        self.f = open("subbeauty.json","w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.f.write(content)
        return item

    def close_spider(self,spider):
        self.f.close()

#beauty img download url
class BeautyDownloadPipeline:
    def __init__(self):
        self.f = open("beauty_download_url.json","w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.f.write(content)
        return item

    def close_spider(self,spider):
        self.f.close()

class BeautyDownloadMysqlPipeline:
    def __init__(self):
        self.db = pymysql.connect('db-server','root','picanoc1119','myspider')
        self.cursor = self.db.cursor()
    def process_item(self,item,spider):
        #insert sql
        insert_sql = 'insert into beauty_download_urls (beauty_name,beauty,url) values (%s,%s,%s)'
        data = dict(item)
        try:
            self.cursor.execute(insert_sql,(data['beauty_name'],data['beauty'],data['url']))
            self.db.commit()
        except Exception as e:
            print(e)
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()

#下载图片pipeline
class SaveImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        dir_name = item['beauty']
        yield scrapy.Request(url=item['url'], meta={'dir_name': dir_name})

    def file_path(self, request, response=None, info=None):
        #接收上面meta传递过来的图片名称
        # 我写的图片名
        dir_name = request.meta['dir_name']

        # 根据情况来选择,如果保存图片的名字成一个体系,那么可以使用这个
        image_name = request.url.split('/')[-1]

        # 清洗Windows系统的文件夹非法字符，避免无法创建目录
        folder_strip = str(dir_name)

        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        filename = u'{0}/{1}'.format(folder_strip, image_name)# 如果有体系,可以使用这个
        #filename = u'{0}'.format(folder_strip)

        return filename


    def item_completed(self, results, item, info):
        # 是一个元组，第一个元素是布尔值表示是否成功
        # if not results[0][0]:
        #     with open('img_error.txt', 'a')as f:
        #         error = str(item['tag'] + ' ' + item['img_url'])
        #         f.write(error)
        #         f.write('\n')
        #         raise DropItem('下载失败')
        return item

#baidu新闻
class MyspiderPipeline:
    def __init__(self):
        self.f = open("news.json","w")

    def process_item(self, item, spider):
        content = json.dumps(dict(item),ensure_ascii=False)+'\n'
        self.f.write(content)
        return item

    def close_spider(self,spider):
        self.f.close()

#保存到mysql数据库中百度新闻
class CustomPipeline:
    def __init__(self):
        self.db = pymysql.connect('localhost','root','picanoc1119','myspider')
        self.cursor = self.db.cursor()
    def process_item(self,item,spider):
        #insert sql
        insert_sql = 'insert into baidunews (title,url,search_num) values (%s,%s,%s)'
        data = dict(item)
        print(data)
        try:
            self.cursor.execute("select version()")
            print(self.cursor.fetchall())
            self.cursor.execute(insert_sql,(data['title'],data['url'],data['search_num']))
            self.db.commit()
        except Exception as e:
            print(e)
        return item
    def close_spider(self,spider):
        self.cursor.close()
        self.db.close()



