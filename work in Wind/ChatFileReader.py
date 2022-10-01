import struct


#####################################################Setting
input_file_path='./ChatUnconfirm.dump'

#####################################################Def data
tempath=input_file_path[0:-5]
output_file_path=tempath+'.txt'

#########################################################Result Data
ChatDict = {}
AckDict = {}
MsgCnt=0
AckCnt=0
TotalCnt=0

try:
    #####################################################open file
    f=open(input_file_path,'rb')


    #####################################################Parse file
    while True:
        uChar=f.read(1)
        if len(uChar) <= 0:
            break
        msgOrAck,=struct.unpack('B',uChar)

        if 11 == msgOrAck :
            f.read(4+4+4+1)

            uShort=f.read(2)
            sdTimeLen,=struct.unpack('H',uShort)
            sendMsgTime=f.read(sdTimeLen)
            sendMsgTime = sendMsgTime[0:8]

            uShort=f.read(2)
            TagLen,=struct.unpack('H',uShort)
            f.read(TagLen)

            uShort=f.read(2)
            strLen,=struct.unpack('H',uShort)
            f.read(strLen)

            MsgCnt = MsgCnt + 1
            if sendMsgTime in ChatDict:
                ChatMsgCnt = ChatDict[sendMsgTime]
                ChatDict[sendMsgTime] = ChatMsgCnt + 1
            else:
                ChatMsgCnt = 1
                ChatDict[sendMsgTime] = ChatMsgCnt

        elif 22 == msgOrAck:
            uInt=f.read(4+4)

            uShort=f.read(2)
            TagLen,=struct.unpack('H',uShort)
            f.read(TagLen)

            uShort=f.read(2)
            ackTimeLen,=struct.unpack('H',uShort)
            ackMsgTime=f.read(ackTimeLen)
            ackMsgTime=ackMsgTime[0:10]

            AckCnt = AckCnt + 1
            if ackMsgTime in AckDict:
                AckMsgCnt = AckDict[ackMsgTime]
                AckDict[ackMsgTime] = AckMsgCnt + 1
            else:
                AckMsgCnt = 1
                AckDict[ackMsgTime] = AckMsgCnt

        else:
            continue

finally:
    f.close()


###############################################################Output record set to file
TotalCnt=MsgCnt+AckCnt
with open(output_file_path,'w') as ff:
    strMsgCnt = 'Chat message count: ' + str(MsgCnt) + '\n'
    strAckCnt = 'Ack message count: ' + str(AckCnt) + '\n'
    strTotalCnt = 'Total message count: ' + str(TotalCnt) + '\n\n'
    ff.write(strMsgCnt)
    ff.write(strAckCnt)
    ff.write(strTotalCnt)
    
    ###########################Output ChatMsg
    ff.write('now output chat message data:\n')
    for key in ChatDict:
        ff.write('SendTime : ' + key + ', count : ' + str(ChatDict[key]) + '\n')
    ff.write('\n')

    ###########################Output AckMsg
    ff.write('now output ack message data:\n')
    for key in AckDict:
        ff.write('AckMessageTime : ' + key + ', count : ' + str(AckDict[key]) + '\n')
    ff.write('\n')

    ff.close()

print 'Chat message count: ' + str(MsgCnt) + '\n'
print 'Ack message count: ' + str(AckCnt) + '\n'
print 'Total message count: ' + str(TotalCnt) + '\n'
print 'finish.'