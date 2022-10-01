"""
Created: 2021-07-22
@author: Richard Wang
"""
#!/usr/bin/python
#coding=utf-8
import csv

#需要设置的地方
IN_FILE_PATH = "E:\\Hack\\2000W_Data\\2000W\\last50144\\last50144.csv"
OUT_FILE_PATH = "E:\\Hack\\2000W_Data\\2000W\\last50144\\"
COL_TOP_NAME = "Name,CardNo,Descriot,CtfTp,CtfId,Gender,Birthday,Address,Zip,Dirty,District1,District2,District3,District4,District5,District6,FirstNm,LastNm,Duty,Mobile,Tel,Fax,EMail,Nation,Taste,Education,Company,CTel,CAddress,CZip,Family,Version,Uid"
MAX_LINES = 200 * 10000

if __name__ == '__main__':
    fd = open(IN_FILE_PATH, 'r')
    outFileName = 1
    filePath = OUT_FILE_PATH + str(outFileName) + '.txt'
    fout = open(filePath, 'a+')
    print("Create file: " + filePath)
    rd_csv = csv.reader(fd, dialect='excel')
    cnt = 0
    fileFstLine = True
    lineC = ""
    colCnt = 0
    for lst in rd_csv:
        for i in range(len(lst)):
            #字段中含有逗号的用分号替换
            lst[i] = lst[i].replace(",", ";")
            #非邮件字段中含有英文双引号的用空格替换
            if (0 != len(lst[i])) and (i != (len(lst) - 11)):
                lst[i] = lst[i].replace("\"", " ")
            else:
                lst[i] = lst[i].replace("\"", "@")
            #非日期时间字段过滤掉头尾空格，中间多个空格合并为一个
            if (0 != len(lst[i])) and (i != (len(lst) - 2)):
                lst[i] = ' '.join(lst[i].split())
            #处理完整的行，有33个字段的为完整行
            if 33 == len(lst):
                lineC = lineC + lst[i] + ','
                colCnt += 1
            #处理非完整行，可能有断行的情况
            else:
                #处理断行的最后一个字段
                if (len(lst) - 1) == i:
                    #处理到最后一个字段时，如果之前已经处理了32个字段，则说明这是最后一个字段，不能再连接逗号分隔符
                    if 32 == colCnt:
                        lineC = lineC + lst[i]
                        colCnt += 1
                    #处理到最后一个字段时，如果之前没有处理32个字段，则说明下面还有断行，需要加空格，并且不能对列计数
                    else:
                        lineC = lineC + lst[i] + ' '
                #处理断行的非最后一个字段
                else:
                    lineC = lineC + lst[i] + ','
                    colCnt += 1
        #完整一行处理完毕，需要写入文件    
        if 33 == colCnt: 
            lineC = lineC[0:len(lineC)-1]
            fout.write(lineC + '\n')
            lineC = ""
            colCnt = 0
            #文件首行不计数
            if True != fileFstLine:
                cnt += 1
        #每处理10万行数据，如果下面还有数据，需要建立新的文件，关闭已经写好的文件
        if 0 == (cnt % 100000) and cnt < MAX_LINES and True != fileFstLine:
            fout.close()
            outFileName += 1
            filePath = OUT_FILE_PATH + str(outFileName) + '.txt'
            fout = open(filePath, 'a+')
            #需要写入数据Col字段名称
            fout.write(COL_TOP_NAME + '\n')
            print("Create file: " + filePath)
        fileFstLine = False
    fout.close()
    fd.close()
    print("Handle complete!")
