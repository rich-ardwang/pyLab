# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 03:41:50 2021

@author: Richard Wang
@filename: jpgSpider.py
"""

import os
import string
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import json
import re
from concurrent.futures import ThreadPoolExecutor #线程池
import time
import imghdr

ROOT_URL = 'https://xr.imeizi.me/'
FILE_DATA_NAME = 'FileData.txt'
#定义10个线程执行此任务
DL_THREAD_CNT = 30

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66'
    #'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}

def parse_jpg_names(file_url, suite_name):
    #下载FileData.txt文件
    fDataName = './' + suite_name + '/' + FILE_DATA_NAME
    if os.path.exists(fDataName):
        os.remove(fDataName)
    html = requests.get(file_url)
    with open(fDataName, 'wb') as wf:
        wf.write(html.content)
        wf.close()
    #按行读取文件
    with open(fDataName, 'r') as rf:
        list = rf.readlines()
        rf.close()
    return list

def download_suite(suite_name):
    #创建套图文件夹
    suiteUrl = suite_name.strip()
    suiteName = suite_name.strip()
    suiteName = suiteName.replace('/', '_')
    suitePath = './' + suiteName + '/'
    if not os.path.exists(suitePath):
        os.makedirs(suitePath, exist_ok=True)
    #获取套图中所有的jpg文件列表
    prefix = ROOT_URL + 'pic/' + suiteUrl + '/'
    orgFdUrl = prefix + FILE_DATA_NAME
    qtFdUrl = quote(orgFdUrl, safe=string.printable)
    jpgList = parse_jpg_names(qtFdUrl, suiteName)
    #下载套图
    for jpg in jpgList:
        jpgName = os.path.basename(jpg.strip())
        fName = './' + suiteName + '/' + jpgName
        if os.path.exists(fName):
            if imghdr.what(fName) is not None:
                continue
        orgJpgUrl = prefix + jpgName
        qtJpgUrl = quote(orgJpgUrl, safe=string.printable)
        jpg_download(qtJpgUrl, fName)

def jpg_download(img_url, file_name):
    print(img_url)
    html = requests.get(img_url)
    #保存图片
    with open(file_name, 'wb') as f:
        f.write(html.content)
        f.close()

def parse_get_suite_name():
    #取得html网页content
    rtHtml = requests.get(ROOT_URL, headers=headers).text
    #将html内容解析为soup对象
    sp = BeautifulSoup(rtHtml, 'html.parser')
    #取得所有script标签
    scriptDoc = sp.find_all('script')
    #只对第11个script标签内容感兴趣，获取var _c = {...};
    jsonList = re.findall(r'^var _c = (.*?)var', scriptDoc[10].__str__(), re.DOTALL | re.MULTILINE)
    #将var _c = {...};清洗为json格式{...}
    jsonText = jsonList[0].replace('var _c = ', '')
    jsonText = jsonText.replace(';', '')
    #载入json格式字串，转为python字典
    data = json.loads(jsonText)
    suiteNameLst = []
    for key in data['dirs']['']['files']:
        suiteNameLst.append(data['dirs']['']['files'][key]['path'])
    return suiteNameLst

def prt_cur_time():
    print(time.strftime("Complete Time: %Y-%m-%d %H:%M:%S", time.localtime()))

def get_jpg_cnt(file_name):
    count = 0
    f = open(file_name, 'r')
    while True:
        line = f.readline()
        if not line:
            break
        else:
            if "" == line.strip():
                continue
            count = count+1
    f.close()
    return count

def check_data():
    dictResult = {}
    filesLst = os.listdir('./')
    for file in filesLst:
        if os.path.isdir(file):
            filesCnt = len(os.listdir(file))
            if filesCnt < 2:
                dictResult[file] = filesCnt
            else:
                curPath = os.path.join('./', file)
                jpgCnt = get_jpg_cnt(curPath + '/' + FILE_DATA_NAME)
                if jpgCnt != filesCnt - 1:
                    dictResult[file] = filesCnt
    with open('./stat.txt', 'wb') as f:
        for k, v in dictResult.items():
            f.write(str("%s >>> %s\n" % (k, v)).encode("utf-8"))
        f.close()

def read_suite_name_from_fl(file_name):
    with open(file_name, 'r') as rf:
        suitNameLst = rf.readlines()
        rf.close()
    return suitNameLst

#有的套图中文件不是jpg文件，把这样的套图名字找到
def get_fake_pic_suite_name():
    lstFiles = []
    filesLst = os.listdir('./')
    for file in filesLst:
        if os.path.isdir(file):
            picsLst = os.listdir(file)
            picsLst.remove(FILE_DATA_NAME)
            for pic in picsLst:
                picName = os.path.join('./', file) + '/' + pic
                if imghdr.what(picName) is None:
                    print(file)
                    lstFiles.append(file)
                    break
    #统计结果记入文件
    with open('./stat.txt', 'wb') as f:
        for stName in lstFiles:
            f.write(str("%s\n" % stName).encode("utf-8"))
        f.close()

if __name__ == '__main__':
    """
    #获取套图path
    #suiteNameLst = parse_get_suite_name()
    suiteNameLst = read_suite_name_from_fl('./stat.txt')
    #多线程下载套图
    tasksLst = []
    threadPool = ThreadPoolExecutor(DL_THREAD_CNT) 
    for stName in suiteNameLst:
        task = threadPool.submit(download_suite, stName)
        tasksLst.append(task)
    #阻塞等待所有任务完成
    for task in tasksLst:
        task.result()
    print('All suite pics complete!!!')
    prt_cur_time()
    print(len(suiteNameLst))
    """
    check_data()
    #get_fake_pic_suite_name()
