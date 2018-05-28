#!/usr/bin/Python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

headers = {
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Encoding": "gzip, deflate, sdch",
	"Accept-Language": "zh-CN,zh;q=0.8,mt;q=0.6",
	"Cache-Control": "max-age=0",
	"Connection": "keep-alive",
	"Host": "sou.zhaopin.com",
	"Referer": "http://www.zhaopin.com/",
	"Upgrade-Insecure-Requests": "1",
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
}


url = 'http://www.baidu.com'

html = requests.get(url, headers=headers).text
print(html)
# soup = BeautifulSoup(html, "html.parser")
#
# logo = soup.select("div")
# print('11111111', logo)

