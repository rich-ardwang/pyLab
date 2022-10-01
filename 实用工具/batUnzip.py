# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
Write by: Vera Archor
Date: 2021-09-19
"""

import os,time

ZIP7="7z.exe x "
BASE_DIR="G:\\games\\3ds\\"
PASS="www.ggfans.net"

def get_zip_files():
    zflst = []
    flst = os.listdir(BASE_DIR)
    for f in flst:
        if os.path.isfile(BASE_DIR+f):
            if '.zip' == os.path.splitext(f)[1]:
                zflst.append(f)
    return zflst

def batch_unzip_files(flst):
    for f in flst:
        fpath=BASE_DIR+f
        fname=os.path.splitext(fpath)[0]
        cmd=ZIP7+'"'+fpath+'" -o"'+fname+'" -p'+PASS
        print(cmd)
        print(fpath+" start to extract...")
        print(os.system(cmd))
        print(fpath+" extract completed.")

if __name__ == "__main__":
    stTime=time.time()
    zfLst=get_zip_files()
    batch_unzip_files(zfLst)
    endTime=time.time()
    print("%d zip files decompressed complete. cost %d seconds." % (len(zfLst), endTime-stTime))