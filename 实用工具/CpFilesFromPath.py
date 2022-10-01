##################################################################################
#Author:         Wang Lei
#FileName:       CpFilesFromPath.py
#Description:    Copy the files which you set from the root path recursively.
#                You can set the file type in varialble Ext, and give the root
#                path and the destination path which you hope to operate.
#Date:           2018-11-08
##################################################################################
import os
import shutil

#You can set the parameters as follow
RootPath='./image2'
DesPath='G://image2_copy'
Ext='.jpg'
##################################################################################
##################################################################################

#Global variables
TotalCnt=0  #Calc total file count

#function defination
def get_all_files(rootdir):
    global TotalCnt
    _files=[]
    list=os.listdir(rootdir)
    for i in range(0,len(list)):
        path=os.path.join(rootdir,list[i])
        if os.path.isdir(path):
            _files.extend(get_all_files(path))
        if os.path.isfile(path):
            if Ext==os.path.splitext(path)[1]:
                _files.append(path)
                TotalCnt=TotalCnt+1
    return _files

def list_all_files(rootdir):
    fileLst=get_all_files(rootdir)
    for i in range(0,len(fileLst)):
        print fileLst[i]
    print "TotalCnt:%d" % TotalCnt

def copy_file(srcfile):
    if not os.path.isfile(srcfile):
        print "%s not exists!" % (srcfile)
    else:
        fname=os.path.split(srcfile)[1]
        dstfile=DesPath+'/'+fname
        shutil.copy2(srcfile,dstfile)

def copy_files(rootdir):
    os.makedirs(DesPath)
    fileLst=get_all_files(rootdir)
    for i in range(0,len(fileLst)):
        copy_file(fileLst[i])
    print "TotalCnt:%d" % TotalCnt
    print "Copy complete."

#Begin to run...
#list_all_files(RootPath)
copy_files(RootPath)
