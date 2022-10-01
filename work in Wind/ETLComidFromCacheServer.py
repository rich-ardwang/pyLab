import datetime
import csv


#########################################################Setting
input_file_path='./Wind.IM.ChatCacheServer.daily.log'


#########################################################Def data
output_file_path='./StatisticCmdId.csv'
time_span=15    #minutes


#########################################################Result Data
CmdId_Tuple=("[EXPO_1501]","[EXPO_1601]","[EXPO_1801]","[EXPO_1833]","[EXPO_1811]","[EXPO_1812]","[EXPO_1813]","[EXPO_1815]","[EXPO_1816]","[EXPO_1818]",
    "[EXPO_1819]","[EXPO_1891]","[MQ_1800]","[MQ_1802]","[MQ_1810]","[MQ_1811]","[MQ_1814]","[MQ_1815]","[MQ_1818]","[Socket_1903]","[Socket_1900]",
    "[Socket_1901]","[Socket_1902]","[Socket_1904]","[Socket_1905]","[Socket_1906]","[Socket_1840]","[Socket_10001802]","[Socket_10001810]","[Socket_10001811]")

Cmdid_Dict={}
TimeSpan_Lst=[]
next_time=""
key_time=""

#########################################################Function define
def is_valid_date(str):
    try:
        datetime.datetime.strptime(str, '%Y-%m-%d %H:%M')
        return True
    except:
        return False

def str2Date(str):
    date=datetime.datetime.strptime(str, '%Y-%m-%d %H:%M')
    return date

def date2Str(date):
    str=date.strftime('%Y-%m-%d %H:%M')
    return str

def FindAndRecordCmdid(strLine,timekey):
    for cid in CmdId_Tuple:
        if -1 != strLine.find(cid):
            if cid not in Cmdid_Dict:
                Cmdid_Dict[cid]={}
                Cmdid_Dict[cid][timekey]=1
            else:
                if timekey not in Cmdid_Dict[cid]:
                    Cmdid_Dict[cid][timekey]=1
                else:
                    cnt=Cmdid_Dict[cid][timekey]
                    Cmdid_Dict[cid][timekey]=cnt+1
            return
        else:
            continue
    return


print "Start to read log file and do some statistic..."


try:
    #####################################################open file
    f=open(input_file_path,'r')

    #####################################################read file
    bFlag = True
    while True:
        line=f.readline()
        if not line:
            break

        time=line[0:16]
        if True == is_valid_date(time):
            if True == bFlag:
                key_time=time
                TimeSpan_Lst.append(key_time)
                dtNow=str2Date(time)
                dtNext=dtNow+datetime.timedelta(minutes=time_span)
                next_time=date2Str(dtNext)
                bFlag=False
            else:
                if time >= next_time:
                    key_time=next_time
                    TimeSpan_Lst.append(key_time)
                    dtNow=str2Date(next_time)
                    dtNext=dtNow+datetime.timedelta(minutes=time_span)
                    next_time=date2Str(dtNext)
            FindAndRecordCmdid(line, key_time)
        else:
            continue

finally:
    #####################################################close file
    f.close()


print "Now output the statistic result of cmdid for CacheServer to the file..."


###############################################################Output record set to csv file
csvFile=open(output_file_path,'wb')

###########################Output ChatMsg
writer=csv.writer(csvFile)

#Col name
TimeSpan_Lst.sort()
ColLst=TimeSpan_Lst[:]
ColLst.insert(0,"Cmdid")
writer.writerow(ColLst)

#Data
keys=Cmdid_Dict.keys()
keys.sort()
for key in keys:
    cid=key[1:-1]
    i=0
    row=[]
    for i in range(len(TimeSpan_Lst)+1):
        if 0==i:
            row.insert(0,cid)
        else:
            strTimeSpan=TimeSpan_Lst[i-1]
            if strTimeSpan in Cmdid_Dict[key]:
                row.insert(i,Cmdid_Dict[key][strTimeSpan])
            else:
                row.insert(i,0)
    writer.writerow(row)

#Close csv file
csvFile.close()


print "Finish!"