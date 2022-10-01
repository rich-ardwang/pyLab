# -*- coding: utf-8 -*-
"""
Created on Mon May 31 19:36:23 2021

@file:      bzSpider.py
@function:  Download video files from Bilibili working as spider mode.
@author:    Richard Wang
@version:   1.0
"""

import os, sys
import re, json, requests
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
    #'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}

#主模块执行
if __name__ == "__main__":
    #参数收集
    if len(sys.argv) != 4:
        print('python bzSpider.py <target_url> <output_path> <start_idx>')
        sys.exit()
    #开始Page索引
    startIdx = int(sys.argv[3])
    if startIdx < 1:
         startIdx = 1
    #输出目录
    if '/' != sys.argv[2][-1]:
        sys.argv[2] = sys.argv[2] + '/'
    targetDir = sys.argv[2]
    #资源首页URL
    targetURL = sys.argv[1]
    #下载baseURL
    baseURL = targetURL[0:targetURL.index('?')] + '?p='
    #取得html网页content
    rtHtml = requests.get(targetURL, headers=headers).text
    #将html内容解析为soup对象
    sp = BeautifulSoup(rtHtml, 'html.parser')
    #匹配出<script>window.__INITIAL_STATE__:{};...</script>
    scriptDoc = sp.find('script', text=re.compile('window\.__INITIAL_STATE__'))
    #利用正则进一步找出"pages":与,"subtitle"中间的部分
    ltxt = re.findall(r'\"pages\"\:(.*?),\"subtitle\"', scriptDoc.__str__(), re.DOTALL | re.MULTILINE)
    #制造出完整的json字符串
    jsonText = "{\"pages\":" + ltxt[0] + "}"
    #json字符串转为python字典
    data = json.loads(jsonText)
    #循环下载多个视频文件
    for i in range(startIdx-1, len(data['pages'])):
        #页数转为string
        sPage = str(data['pages'][i]['page'])
        #过滤掉part名称中的所有空格
        name = data['pages'][i]['part'].replace(" ", "")
        #设置下载URL
        dlURL = baseURL + sPage
        #设置文件path+filename
        fileName = targetDir + "P" + sPage + "-" + name
        print("Download: " + dlURL + ", " + fileName + " ...")
        print(os.system("you-get " + dlURL + " -O " + fileName))
    #执行完毕
    print("执行完毕！")