import time
from lxml import etree
import scrapy
from scrapy.http import Request
import json
from chaojiying import Chaojiying_Client
import execjs
import requests
import time
import os
from bs4 import BeautifulSoup

class Cookie:
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def getCookies(self):
        list = []
        session = requests.session()
        # 设置请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }
        # 请求的网页
        url1 = 'http://cas.swust.edu.cn/authserver/login'
        # url1 = 'http://cas.swust.edu.cn/authserver/login?service=http://myo.swust.edu.cn/mht_shall/a/service/serviceFrontManage/cas'

        h = session.get(url=url1, headers=headers,verify=False)
        HTML = etree.HTML(h.text)

        execution = HTML.xpath('//*[@id="fm2"]/ul/li[1]/input[1]/@value')[0]
        # print(execution)
        # 获取解密模板
        getKey = 'http://cas.swust.edu.cn/authserver/getKey'

        h = session.get(url=getKey, headers=headers,verify=False)

        Modulus = h.json()['modulus']

        # 获取验证码并识别验证码
        captcha = 'http://cas.swust.edu.cn/authserver/captcha?timestamp={}'.format(int(time.time() * 1000))
        h = session.get(url=captcha, headers=headers,verify=False)
        captcha = self.VertifCode(h.content)


        # 解密密码
        password  = self.dePassword(self.password,Modulus)

        # 填写表单登录
        login = 'http://cas.swust.edu.cn/authserver/login?service=http://myo.swust.edu.cn/mht_shall/a/service/serviceFrontManage/cas'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "http://cas.swust.edu.cn/authserver/login?service=http://myo.swust.edu.cn/mht_shall/a/service/serviceFrontManage/cas"
        }
        m = {
            "execution": execution,
            "_eventId": "submit",
            "geolocation": "",
            "username": self.username,
            "lm": "usernameLogin",
            "password": password,
            "captcha": captcha
        }


        # 获取登录界面cookie
        h = session.post(url=login, headers=headers, data=m,verify=False)
        view_index = 'http://myo.swust.edu.cn/mht_shall/a/service/serviceFrontManage#view_index'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
        }
        h = session.get(url=view_index, headers=headers, verify=False)
        cookie1 = session.cookies.get_dict()
        dict1 = {"登录界面":cookie1}
        list.append(dict1)

        # 获取教务平台考试的cookie
        url = 'https://matrix.dean.swust.edu.cn/acadmicManager/index.cfm?event=studentPortal:DEFAULT_EVENT'
        h = session.get(url=url, headers=headers, verify=False)
        # print(h.text)
        cookie2 = session.cookies.get_dict()
        dict2 = {"教务平台":cookie2}
        list.append(dict2)

        return list

    def VertifCode(self,content):
        chaojiying = Chaojiying_Client('12312312312', '956671548asd', '921523')
        result = chaojiying.PostPic(content, 1006)
        return  result['pic_str']

    def dePassword(self,password,Modulus):
        with open(os.getcwd() + '.\security.js', 'r+') as f:
            result = f.read()
        ctx = execjs.compile(result)
        password = ctx.call('aaaa', Modulus, password)
        return password
if __name__ == '__main__':

    username = "5120205915"
    password = "956671548Asd"
    cookie = Cookie(username, password)
    print(cookie.getCookies())