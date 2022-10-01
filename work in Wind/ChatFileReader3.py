import struct


#####################################################Setting
input_file_path='./20180420_00_ChatInfo.db'

#####################################################Def data
tempath=input_file_path[0:-3]
output_file_path=tempath+'.txt'

class chatTime:
    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.usec = 0
        self.res = 0
    def parseFromFile(self, f):
        uInt = f.read(4)
        val, = struct.unpack('I',uInt)
        self.year = val & 4095
        self.month = (val >> 12) & 15
        self.day = (val >> 16) & 31
        self.hour = (val >> 21) & 31
        self.min = (val >> 26) & 63
        uInt = f.read(4)
        val, = struct.unpack('I',uInt)
        self.sec = val & 63
        self.usec = (val >> 6) & 1048575
        self.res = (val >> 26) & 63
    def __str__(self):
        return "%04d-%02d-%02d %02d:%02d:%02d"%(self.year,self.month,self.day,self.hour,self.min,self.sec)


OutputData=[]

try:
    #####################################################open file
    f=open(input_file_path,'rb')


    #####################################################Parse FileHead
    uChar=f.read(1)
    type,=struct.unpack('B',uChar)

    uChar=f.read(1)
    Version,=struct.unpack('B',uChar)

    uChar=f.read(1)
    ByteOrder,=struct.unpack('B',uChar)

    Tag=f.read(13)

    uInt=f.read(4)
    FileHeadCrc,=struct.unpack('I',uInt)

    uInt=f.read(4)
    FileCrc,=struct.unpack('I',uInt)

    uInt=f.read(4)
    FileDBSize,=struct.unpack('I',uInt)

    Reserve=f.read(4)

    uInt=f.read(4)
    DataOffset,=struct.unpack('I',uInt)

    uInt=f.read(4)
    DataSize,=struct.unpack('I',uInt)

    uInt=f.read(4)
    DataWritePos,=struct.unpack('I',uInt)

    uInt=f.read(4)
    RecordCount,=struct.unpack('I',uInt)
    print 'Record count: '+str(RecordCount)

    for t in range(0,RecordCount):
        RecordData=[]
        ########################################################Parse MsgHead
        uShort=f.read(2)
        MsgHeadTag,=struct.unpack('H',uShort)

        uChar=f.read(1)
        MsgHeadType,=struct.unpack('B',uChar)

        uChar=f.read(1)
        MsgHeadValid,=struct.unpack('B',uChar)

        iL=f.read(4)
        MsgHeadLen,=struct.unpack('i',iL)

        ####################################################Parse Data body
        uShort=f.read(2)
        TagLen,=struct.unpack('H',uShort)

        msgTag=f.read(TagLen)
        RecordData.append(msgTag)

        uChar=f.read(1)
        ChatType,=struct.unpack('B',uChar)
        RecordData.append(ChatType)

        msgDateTime=chatTime()
        msgDateTime.parseFromFile(f)
        RecordData.append(msgDateTime)

        uInt=f.read(4)
        SendUserID,=struct.unpack('I',uInt)
        RecordData.append(SendUserID)

        uShort=f.read(2)
        recvCount,=struct.unpack('H',uShort)
        for v in range(0, recvCount):
            uInt=f.read(4)
            RecvUserID,=struct.unpack('I',uInt)
            RecordData.append(RecvUserID)

        uInt=f.read(4)
        strLen,=struct.unpack('I',uInt)

        msgInfo=f.read(strLen)
        RecordData.append(msgInfo)

        uChar=f.read(1)
        Flag,=struct.unpack('B',uChar)
        RecordData.append(Flag)

        AckTime=chatTime()
        AckTime.parseFromFile(f)
        RecordData.append(AckTime)

        #######################################################Parse MsgTail
        uShort=f.read(2)
        MsgTail,=struct.unpack('H',uShort)

        #######################################################Get record set
        OutputData.append(RecordData)

finally:
    f.close()


###############################################################Output record set to file
with open(output_file_path,'w') as ff:
    ss=len(OutputData)
    for i in range(0,ss):
        s=len(OutputData[i])
        for j in range(0,s):
            ff.write(str(OutputData[i][j]))
            ff.write(',')
        ff.write('\n')
    ff.close()

print 'create \"' + output_file_path + '\" finish.'