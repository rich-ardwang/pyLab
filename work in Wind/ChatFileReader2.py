import struct


#####################################################Setting
input_file_path='./ChatUnconfirm.dump'

#####################################################Def data
tempath=input_file_path[0:-5]
output_file_path=tempath+'.txt'


try:
    #####################################################open file
    f=open(input_file_path,'rb')


    #####################################################Parse file
    OutputData=[]
    while True:
        RecordData=[]

        uChar=f.read(1)
        if len(uChar) <= 0:
            break
        msgOrAck,=struct.unpack('B',uChar)

        if 11 == msgOrAck :
            uInt=f.read(4)
            recvIMUserId,=struct.unpack('I',uInt)
            RecordData.append(recvIMUserId)

            uInt=f.read(4)
            userId,=struct.unpack('I',uInt)
            RecordData.append(userId)

            uInt=f.read(4)
            sendIMUserId,=struct.unpack('I',uInt)
            RecordData.append(sendIMUserId)

            uChar=f.read(1)
            chatType,=struct.unpack('B',uChar)
            RecordData.append(chatType)

            uShort=f.read(2)
            sdTimeLen,=struct.unpack('H',uShort)
            sendMsgTime=f.read(sdTimeLen)
            RecordData.append(sendMsgTime)

            uShort=f.read(2)
            TagLen,=struct.unpack('H',uShort)
            msgTag=f.read(TagLen)
            RecordData.append(msgTag)

            uShort=f.read(2)
            strLen,=struct.unpack('H',uShort)
            msgInfo=f.read(strLen)
            RecordData.append(msgInfo)

            OutputData.append(RecordData)

        elif 22 == msgOrAck:
            uInt=f.read(4)
            recvIMUserId,=struct.unpack('I',uInt)
            RecordData.append(recvIMUserId)

            uInt=f.read(4)
            userId,=struct.unpack('I',uInt)
            RecordData.append(userId)

            uShort=f.read(2)
            TagLen,=struct.unpack('H',uShort)
            msgTag=f.read(TagLen)
            RecordData.append(msgTag)

            uShort=f.read(2)
            ackTimeLen,=struct.unpack('H',uShort)
            ackMsgTime=f.read(ackTimeLen)
            RecordData.append(ackMsgTime)

            OutputData.append(RecordData)

        else:
            continue

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