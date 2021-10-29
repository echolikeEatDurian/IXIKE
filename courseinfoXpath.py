from lxml import etree


with open('./courseinfo.html','rt',encoding='utf-8') as fp:
    text = fp.read()

response = etree.HTML(text)

dict ={}
courseTrs = response.xpath('//*[@class = "UICourseTable"]/tbody/tr')
for courseTr in courseTrs:
    courseTds = courseTr.xpath('./td')
    for courseTd in courseTds:
        div = courseTd.xpath('./div')
        if len(div) != 0:
            courseinfomation = courseTd.xpath('./div')[0]
            dict['coursename'] = courseinfomation.xpath('./span[@class="course"]/text()')[0].strip()
            dict['teachername'] = courseinfomation.xpath('./span[@class="teacher"]/text()')[0].strip()
            dict['place'] = courseinfomation.xpath('./span[@class="place"]/text()')[0].strip()

            data = courseinfomation.xpath('./span[@class="week"]/text()')[0].split('-')
            start = int(data[0])
            end = int(data[1][:2])
            dict['startAndEnd'] = [i for i in range(start,end+1)]


            print(dict)
    print('')
