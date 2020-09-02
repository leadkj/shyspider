#注意：
##settings.py中
###1.改为false ,不然robots 拒绝爬取

ROBOTSTXT_OBEY = False  

###2,添加header
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

###3，items中的类对象是字典方式调用
这种方式错误
```python
            item.title = title
            item.url = url
            item.search_num = search_num
```

这样使用
```python
            item['title'] = title
            item['url']= url
            item['search_num'] = search_num
```

###4，定义多个pipline ，即保存数据到多个存储
```python
ITEM_PIPELINES = {
    #字典中每个key表示一种pipline,value 表示优先级，1-1024，越小越高
   'MySpider.pipelines.MyspiderPipeline': 300,
   'MySpider.pipelines.CustomPipeline': 200,
}
```