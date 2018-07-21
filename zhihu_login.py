# -*- coding: utf-8 -*-
import requests
from parsel import Selector
import json
import time
from copyheaders import headers_raw_to_dict
import execjs
from requests_toolbelt.multipart.encoder import MultipartEncoder

class Login_zhihu(object):
    def __init__(self,session):
        self.session=session
    def getdata(self,username, password, captcha=''):
        client_id = 'c3cef7c66a1843f8b3a9e6a1e3160e20'
        timestamp = int(time.time()) * 1000
        with open('signature.js','r',encoding='utf-8') as f:
            signature_js=f.read()
        js1 = execjs.compile(signature_js)
        signature = js1.call('run', 'password', timestamp)
        data = {
            'client_id': client_id, 'grant_type': 'password',
            'timestamp': str(timestamp), 'source': 'com.zhihu.web',
            'signature': signature, 'username': username,
            'password': password, 'captcha': captcha,
            'lang': 'en', 'ref_source': 'homepage', 'utm_source': ''
        }
        return data
       
    def getheaders(self,session):
        '从网页源代码内解析出 uuid与Xsrftoken'

        z1 = self.session.get('https://www.zhihu.com/')
        sel = Selector(z1.text)
        jsdata = sel.css('div#data::attr(data-state)').extract_first()
        xudid = json.loads(jsdata)['token']['xUDID']
        xsrf = json.loads(jsdata)['token']['xsrf']
        post_headers_raw = b'''
        accept:application/json, text/plain, */*
        Accept-Encoding:gzip, deflate, br
        Accept-Language:zh-CN,zh;q=0.9,zh-TW;q=0.8
        authorization:oauth c3cef7c66a1843f8b3a9e6a1e3160e20
        Connection:keep-alive
        DNT:1
        Host:www.zhihu.com
        Origin:https://www.zhihu.com
        Referer:https://www.zhihu.com/signup?next=%2F
        User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36
        '''
        headers = headers_raw_to_dict(post_headers_raw)
        headers['X-UDID'] = xudid
        headers['X-Xsrftoken'] = xsrf
        return headers


    def checkcapthca(self,headers, cn=True):
        '检查是否需要验证码,无论需不需要，必须要发一个请求'
        if cn:
            url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
        else:
            url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        headers.pop('X-Xsrftoken')
        z = self.session.get(url, headers=headers)
        return z.json()

    def login(self,username, password):
        url = 'https://www.zhihu.com/api/v3/oauth/sign_in'

        headers = self.getheaders(session)
        data = self.getdata(username, password)
        self.checkcapthca(headers)
        # multipart_encoder = MultipartEncoder(fieles=data, boundary='----WebKitFormBoundarycGPN1xiTi2hCSKKZ')
        # todo:boundary后面的几位数可以随机，现在是固定的
        encoder = MultipartEncoder(data, boundary='----WebKitFormBoundarycGPN1xiTi2hCSKKZ')
        headers['Content-Type'] = encoder.content_type
        #z2 = s.post(url, headers=headers, data=encoder.to_string(), )
        z2 = self.session.post(url, headers=headers, data=encoder.to_string(), )
        with open ('cookies.json','w') as f:
            json.dump(requests.utils.dict_from_cookiejar(self.session.cookies),f)
session=requests.session()
session.headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}

a=Login_zhihu(session)
a.login('user','password')



