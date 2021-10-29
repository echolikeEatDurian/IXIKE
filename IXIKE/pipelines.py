# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

class IxikePipeline:

    def open_spider(self,spider): # 爬虫开始的时候启动数据库

        self.conn = pymysql.connect(user='root',password='12345',host = 'localhost',database='swustinfo')
        self.cursor = self.conn.cursor()


    def process_item(self, item, spider):

        username = item['username']
        coursename = item['coursename']
        teachername = item['teachername']
        weekAndsection = item['weekAndsection']
        startAndEnd = item['startAndEnd']
        place = item['place']


        sql = "insert into course values ('{}','{}','{}','{}','{}','{}')".format(username, coursename, teachername,
                                                                                 weekAndsection, startAndEnd, place)
        self.cursor.execute(sql)
        print(sql)
        self.conn.commit()
        # 爬虫结束时的操作
    def close_spider(self,spider):
        self.cursor.close()
        self.conn.close()