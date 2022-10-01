# -*- coding:utf-8 -*-
"""
Created on Mon June 01 13:07:01 2021

@file:      batRename.py
@function:  
@author:    Richard Wang
@version:   1.0
"""

import os

#指定目录，要加'/'，否则解析失败
path = '\\\\192.168.1.14\\资料大全\\技术课程视频\\黑客技术\\2021最新KaliLinux渗透高级篇-780集持续更新\\'

#主模块执行
if __name__ == "__main__":
    #获取该目录下所有文件，存入列表
    fLst = os.listdir(path)
    #按文件名中的数字排序，排序前将数字截取出转为float
    #fLst.sort(key=lambda x:int(x.split('-')[0].split('P')[1]))
    fLst.sort(key=lambda x:float(x.split('-')[0]))
    n = 0
    for i in fLst:
        #设置旧文件名(路径+文件名)
        oldName = path + fLst[n]
        #设置新文件名
        newName = path + 'P' + str(n + 1) + '-' + fLst[n]
        #newName = path + 'P' + str(n + 1) + '-' + fLst[n].split('-', 1)[1]
        #用os模块中rename方法重命名
        os.rename(oldName, newName)
        print(oldName, '=====>', newName)
        #print(newName)
        n += 1
    print('complete!')