#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created: 2021-06-29
@author: Richard Wang
"""

import sys
import os
import time
from multiprocessing.dummy import Pool
from PIL import Image


rmOrg = True
def convert(pic, imgFormat):
    name = os.path.splitext(pic)[0]
    webp_im = Image.open(pic)
    rgb_im = webp_im.convert('RGB')
    new_name = name + imgFormat
    rgb_im.save(new_name)
    #转换格式后删除，如果不需要删除原来的webp文件，直接注释即可
    if rmOrg:
        os.remove(pic)

#tiny_png批量将文件夹下的webp文件转换为png格式
def tiny_png(pic):
    convert(pic, '.png')

def folder(target_path):
    begin_time = int(time.time())
    #path = os.path.abspath('.')
    pics = [os.path.join(target_path, x) for x in os.listdir(target_path) if os.path.isfile(os.path.join(target_path, x)) and (os.path.splitext(x)[1] == '.webp')]
    #pics = [x for x in os.listdir('.') if os.path.isfile(x) and (os.path.splitext(x)[1] == '.png') or (os.path.splitext(x)[1] == '.jpg')]
    #print(pics)
    #exit(0)
    if not pics:
        print('no images in this folder！')
        return
    pool = Pool(3)
    result = pool.map(tiny_png, pics)
    #记录工作耗时
    end_time = int(time.time())
    spend_time = end_time - begin_time
    print('process is over and it costs ' + str(spend_time) + ' senconds')

if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('python webpConvert.py <file_abs_path> [remove_org_file:1 or 0]')
        sys.exit()
    if len(sys.argv) == 3:
        if '0' == sys.argv[2]:
            rmOrg = False
        else:
            rmOrg = True
    print('Start to convert. Path:' + sys.argv[1])
    folder(sys.argv[1])