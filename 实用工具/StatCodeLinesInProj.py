# -- coding: utf-8 --
######################################################################
#功能：代码行数统计，可以递归目录
#作者：Richard Wang
#时间：2018/08/30
#版本：python 2.7
#使用说明：
#      ROOT_PATH：配置source目录，会自动递归统计所有文件代码行数总和
#      INCLUDE_EMPTY_LINE：True时则将空行列入统计，否则空行不予统计
#      ALL_FILE：True时则统计所有文件，否则只统计指定扩展名的文件
#      EXT：指定需要统计的文件扩展名
#      IGNORE_DIR：指定需要忽略的目录，无忽略目录置为空
######################################################################
import os


#########################Settings##################################
#ROOT_PATH="D:\\GoLab\\src\\github.com\\hyperledger\\fabric"
ROOT_PATH="D:\\VCLab\\redis"
INCLUDE_EMPTY_LINE=False
ALL_FILE=False
#EXT=['.go']
#IGNORE_DIR=['vendor', 'unit-test', 'test', 'scripts',
#        'sampleconfig', 'release_notes', 'release', 'proposals',
#        'images', 'gotools', 'docs', 'bddtests', 'devenv',
#        'examples', '.idea', '.git']
EXT=['.h','.c']
IGNORE_DIR=[]
###################################################################

def IsDefFile(file_path):
    extname=os.path.splitext(file_path)[1]
    for e in EXT:
        if extname==e:
            return True
    return False

def IsIgnoreDir(ignore_dir):
    for d in IGNORE_DIR:
        if ignore_dir==d:
            return True
    return False

def StatCodeLine(file_path,include_empty_line,code_line_cnt):
    count=code_line_cnt
    if os.path.isdir(file_path) :
        files=os.listdir(file_path)
        for file in files:
            tmp_path=os.path.join(file_path,file)
            #print tmp_path
            if not os.path.isdir(tmp_path):
                if not ALL_FILE:
                    if not IsDefFile(tmp_path):
                        continue
                count=count+StatFileLine(tmp_path,include_empty_line)
            else:
                if IsIgnoreDir(file):
                    continue
                count=StatCodeLine(tmp_path,include_empty_line,count)
    else:
        count=count+StatFileLine(file_path,include_empty_line)
    return count

def StatFileLine(file_name,include_empty_line):
    count=0
    f=open(file_name,'r')
    while True:
        line=f.readline()
        if not line:
            break
        else:
            if True!=include_empty_line :
                if ""==line.strip() :
                    continue
            count=count+1
    f.close()
    return count

if __name__ == "__main__":
    StatCount=StatCodeLine(ROOT_PATH,INCLUDE_EMPTY_LINE,0)
    print "Total code line count : " + str(StatCount)
