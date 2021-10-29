import scrapy
from COOKIE import Cookie
from IXIKE.items import IxikeItem
from lxml import etree
username = "5120205915"
password = "956671548Asd"
cookie = Cookie(username, password)

cookies = cookie.getCookies()
print(cookies)


# print(cookies[0]['教务平台'])

class IxikeSpider(scrapy.Spider):
    name = 'ixike'
    # allowed_domains = ['swust.com']
    start_urls = ['https://matrix.dean.swust.edu.cn/acadmicManager/index.cfm?event=studentPortal:courseTable']

    # 重写start_requests方法
    def start_requests(self):
        return [ scrapy.Request(url=self.start_urls[0], cookies=cookies[1]['教务平台'] )]

    def parse(self, response):
        dict = IxikeItem()
        dict['weekAndsection'] = 0
        dict['username'] = 0
        source = etree.HTML(response.text)
        courseTrs = source.xpath('//*[@class = "UICourseTable"]/tbody/tr')# 获得课程的遍历TR
        # print(courseTrs,type(courseTrs))
        for courseTr in courseTrs:
            courseTds = courseTr.xpath('./td')# 解析每个tr下的td
            for courseTd in courseTds:
                div = courseTd.xpath('./div') # 解析每个td下的div
                if len(div) != 0:
                    courseinfomation = courseTd.xpath('./div')[0]
                    dict['coursename'] = courseinfomation.xpath('./span[@class="course"]/text()')[0].strip()
                    dict['teachername'] = courseinfomation.xpath('./span[@class="teacher"]/text()')[0].strip()
                    dict['place'] = courseinfomation.xpath('./span[@class="place"]/text()')[0].strip()
                    data = courseinfomation.xpath('./span[@class="week"]/text()')[0].split('-')
                    start = int(data[0])
                    end = int(data[1][:2])
                    dict['startAndEnd'] = [i for i in range(start, end + 1)]
                    print(dict)
                    yield  dict
        # for i in range(36):
        #     dict['coursename'] = i
        #     dict['username'] = i
        #     dict['teachername'] = i
        #     dict['place'] = i
        #     dict['startAndEnd'] = i
        #     dict['weekAndsection'] = i
        #     yield dict








