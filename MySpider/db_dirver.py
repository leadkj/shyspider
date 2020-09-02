import pymysql
from redis import Redis
import json
from pymongo import MongoClient
from gridfs import *
import os


class MysqlDB():
	def __init__(self):
		self.host = 'db-server'
		self.port = '3306'
		self.user = 'root'
		self.passwd = 'picanoc1119'
		self.db = 'myspider'
	def connect(self):
		try:
			driver = pymysql.connect(self.host,self.user,self.passwd,self.db)
		except Exception as e:
			raise e
		return driver

	def exec_sql(self,sql):
		driver = self.connect()
		try:
			cursor = driver.cursor()
			cursor.execute(sql)
			driver.commit()
		except Exception as e:
			raise e
	def finish(self):
		dirver = self.connect()
		dirver.close()
class RedisDB():
	def __init__(self):
		self.host = 'db-server'
		self.port = 6379
		self.db = 0
	def connect(self):

		driver = Redis(host=self.host,port=self.port,db=self.db)
		return  driver
	def do_somthing(self):
		driver = self.connect()
		#redis_data_list = "pics:start_urls"
		down_load_key = "imgsrc:start_urls"

		with open('data/beauty.json') as f:
			for line in f.readlines():
				if line.strip():
					url = json.loads(line)['url']
					if url.startswith("https"):
						driver.lpush(down_load_key ,url)





#Mongodb
class MongoDB():
	def __init__(self,db):
		#链接mongodb
		self.client=MongoClient('db-server',27017)
		self.db = self.client[db]
	def uploadImg(self,dirs):
		#本地硬盘上的图片目录
		#dirs = 'e:\cs'
		#列出目录下的所有图片
		files = os.listdir(dirs)
		#遍历图片目录集合
		for file in files:
			#图片的全路径
			filesname = dirs + '\\' + file
			#分割，为了存储图片文件的格式和名称
			f = file.split('.')
			#类似于创建文件
			datatmp = open(filesname, 'rb')
			#创建写入流
			imgput = GridFS(self.db)
			#将数据写入，文件类型和名称通过前面的分割得到
			insertimg=imgput.put(datatmp,content_type=f[1],filename=f[0])
			datatmp.close()
			print("js")
	def loadImg(self):
		gridFS = GridFS(self.db, collection="fs")
		count = 0
		for grid_out in gridFS.find():
			count += 1
			print(count)
			data = grid_out.read()  # 获取图片数据
			outf = open('cs{}.jpg'.format(count), 'wb')  # 创建文件
			outf.write(data)  # 存储图片
			outf.close()

# rdb = RedisDB()
# rdb.do_somthing()


#mdb = MongoDB('image')

#---上传图片到mongodb
#dirs=r'D:\pydev\MySpider\data\beauty\224448'
#mdb.uploadImg(dirs)

#---下载图片到本地
#mdb.loadImg()



# video_db = MongoDB("video")
# dir = 'F:\COBBLER\secret'
# video_db.uploadImg(dir)

mydb = MysqlDB()
with open('data/beauty.json') as f:
	for line in f.readlines():
		res = json.loads(line)
		sql = "insert into bid_cid (beauty,category) values (\'%s\',\'%s\')" %(res['category'],res['beauty'])
		mydb.exec_sql(sql)
mydb.finish()