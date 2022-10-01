#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun May 23 22:49:49 2021

@author: Richard Wang
"""

import sys
import hashlib

def get_file_md5(file_name):
    """
    计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()   #创建md5对象
    with open(file_name,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  #更新md5对象
    return m.hexdigest()    #返回md5对象

def get_str_md5(content):
    """
    计算字符串md5
    :param content:
    :return:
    """
    m = hashlib.md5(content.encode('utf-8')) #创建md5对象
    return m.hexdigest()

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('python md5.py -f <file_name> or python md5.py <target string>')
        sys.exit()
    if len(sys.argv) == 2:
        print(get_str_md5(sys.argv[1]))
    else:
        print(get_file_md5(sys.argv[2]))