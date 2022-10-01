# -*- coding: utf-8 -*-
"""
Created on Mon June 1st 01:16:18 2021

@file:      execCmdTest.py
@function:  Test executing the command line in python code.
@author:    Richard Wang
@version:   1.0
"""

import os

#下载baseURL
baseURL = 'https://www.bilibili.com/video/BV1SA411G7aF?p='

#主模块执行
if __name__ == "__main__":
    dlURL = baseURL + "1"
    print(dlURL)
    print(os.system("you-get " + dlURL + " -O ../mp4/123"))
