# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IxikeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    """
    usename:账户名
    coursename:课程的名字
    teachername:教师姓名
    weekAndSection:星期几第几节课
    startAndEnd:开始结束的日期
    place：上课的地点

    """
    username = scrapy.Field()
    coursename = scrapy.Field()
    teachername = scrapy.Field()
    weekAndsection = scrapy.Field()
    startAndEnd = scrapy.Field()
    place = scrapy.Field()