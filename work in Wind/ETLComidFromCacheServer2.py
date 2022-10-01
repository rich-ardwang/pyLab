#########################################################Setting
input_file_path='./Wind.IM.ChatCacheServer.daily.log'


#########################################################Def data
output_file_path='./StatisticCmdIdForCacheSrv.txt'


#########################################################Result Data
CmdId = {}
CmdId["[EXPO_1501]"]=0
CmdId["[EXPO_1601]"]=0
CmdId["[EXPO_1801]"]=0
CmdId["[EXPO_1833]"]=0
CmdId["[EXPO_1811]"]=0
CmdId["[EXPO_1812]"]=0
CmdId["[EXPO_1813]"]=0
CmdId["[EXPO_1815]"]=0
CmdId["[EXPO_1816]"]=0
CmdId["[EXPO_1818]"]=0
CmdId["[EXPO_1819]"]=0
CmdId["[EXPO_1891]"]=0
CmdId["[MQ_1800]"]=0
CmdId["[MQ_1802]"]=0
CmdId["[MQ_1810]"]=0
CmdId["[MQ_1811]"]=0
CmdId["[MQ_1814]"]=0
CmdId["[MQ_1815]"]=0
CmdId["[MQ_1818]"]=0
CmdId["[Socket_1903]"]=0
CmdId["[Socket_1900]"]=0
CmdId["[Socket_1901]"]=0
CmdId["[Socket_1902]"]=0
CmdId["[Socket_1904]"]=0
CmdId["[Socket_1905]"]=0
CmdId["[Socket_1906]"]=0
CmdId["[Socket_1840]"]=0
CmdId["[Socket_10001802]"]=0
CmdId["[Socket_10001810]"]=0
CmdId["[Socket_10001811]"]=0


#########################################################Function define
def FindAndRecordCmdid(strLine):
    for key in CmdId:
        if -1 != strLine.find(key):
            cnt=CmdId[key]
            CmdId[key]=cnt+1
            return
        else:
            continue
    return


print "Start to read log file and do some statistic..."


try:
    #####################################################open file
    f=open(input_file_path,'r')

    #####################################################read file
    while True:
        line=f.readline()
        if not line:
            break
        FindAndRecordCmdid(line)

finally:
    #####################################################close file
    f.close()


print "Now output the statistic result of cmdid for CacheServer to the file..."


###############################################################Output record set to file
with open(output_file_path,'w') as ff:
    ###########################Output ChatMsg
    ff.write('Now output the statistic result of cmdid for CacheServer...\n')
    keys=CmdId.keys()
    keys.sort()
    for key in keys:
        cid=key[1:-1]
        ff.write('CmdId : ' + cid.ljust(20) + 'count : ' + str(CmdId[key]) + '\n')
    ff.write('\n')

    ff.close()


print "Finish!"