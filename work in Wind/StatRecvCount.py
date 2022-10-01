import struct


#####################################################Setting
input_file_path='./ChatUnconfirm.dump'


#####################################################Def data
output_chatmsgfile_path='StatChatMsg.txt'
output_ackmsgfile_path='StatAckMsg.txt'

#########################################################Result Data
RecvIdMsgDict={}
RecvIdAckDict={}
MsgCnt=0
AckCnt=0
TotalCnt=0


print 'Start to read file...'
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
            uInt=f.read(4)
            recvIMUserId,=struct.unpack('I',uInt)

            uInt=f.read(4)
            userId,=struct.unpack('I',uInt)

            uInt=f.read(4)
            sendIMUserId,=struct.unpack('I',uInt)

            uChar=f.read(1)
            chatType,=struct.unpack('B',uChar)

            uShort=f.read(2)
            sdTimeLen,=struct.unpack('H',uShort)
            f.read(sdTimeLen)

            uShort=f.read(2)
            TagLen,=struct.unpack('H',uShort)
            f.read(TagLen)

            uShort=f.read(2)
            strLen,=struct.unpack('H',uShort)
            f.read(strLen)

            if 0 != userId :
                MsgCnt=MsgCnt+1
                if recvIMUserId not in RecvIdMsgDict:
                    RecvIdMsgDict[recvIMUserId]={}
                if sendIMUserId not in RecvIdMsgDict[recvIMUserId]:
                    RecvIdMsgDict[recvIMUserId][sendIMUserId]=0
                else:
                    mCnt=RecvIdMsgDict[recvIMUserId][sendIMUserId]
                    RecvIdMsgDict[recvIMUserId][sendIMUserId]=mCnt+1

        elif 22 == msgOrAck:
            uInt=f.read(4)
            recvIMUserId,=struct.unpack('I',uInt)

            uInt=f.read(4)
            userId,=struct.unpack('I',uInt)

            uShort=f.read(2)
            TagLen,=struct.unpack('H',uShort)
            f.read(TagLen)

            uShort=f.read(2)
            ackTimeLen,=struct.unpack('H',uShort)
            f.read(ackTimeLen)

            AckCnt = AckCnt + 1

            if recvIMUserId not in RecvIdAckDict:
                RecvIdAckDict[recvIMUserId]={}
            if userId not in RecvIdAckDict[recvIMUserId]:
                RecvIdAckDict[recvIMUserId][userId]=0
            else:
                mCnt=RecvIdAckDict[recvIMUserId][userId]
                RecvIdAckDict[recvIMUserId][userId]=mCnt+1

        else:
            continue

finally:
    f.close()

TotalCnt=MsgCnt+AckCnt
print 'Read file finish.'


###############################################################Output RecvIdMsgDict to file
print 'Start to output RecvIdMsgDict to file...'
with open(output_chatmsgfile_path,'w') as f1:
    strMsgCnt = 'Chat message count: ' + str(MsgCnt) + '\n\n'
    f1.write(strMsgCnt)

    ###########################Output ChatMsg
    f1.write('Now output chat message statistics:\n')
    keysRecv=RecvIdMsgDict.keys()
    keysRecv.sort()
    for keyRecv in keysRecv:
        keysSend=RecvIdMsgDict[keyRecv].keys()
        keysSend.sort()
        for keySend in keysSend:
            f1.write('RecvId : ' + str(keyRecv).ljust(20) + 'SendId : ' +  str(keySend).ljust(20) + 'count : ' + str(RecvIdMsgDict[keyRecv][keySend]) + '\n')
    f1.write('\n')
    f1.close()
print 'Output RecvIdMsgDict to file finish.'


###############################################################Output RecvIdAckDict to file
print 'Start to output RecvIdAckDict to file...'
with open(output_ackmsgfile_path,'w') as f2:
    strAckCnt = 'Ack message count: ' + str(AckCnt) + '\n\n'
    f2.write(strAckCnt)

    ###########################Output AckMsg
    f2.write('Now output ack message statistics:\n')
    keysRecv=RecvIdAckDict.keys()
    keysRecv.sort()
    for keyRecv in keysRecv:
        keysSend=RecvIdAckDict[keyRecv].keys()
        keysSend.sort()
        for keySend in keysSend:
            f2.write('RecvId : ' + str(keyRecv).ljust(20) + 'SendId : ' +  str(keySend).ljust(20) + 'count : ' + str(RecvIdAckDict[keyRecv][keySend]) + '\n')
    f2.write('\n')
    f2.close()
print 'Output RecvIdAckDict to file finish.'

print 'Chat message count: ' + str(MsgCnt)
print 'Ack message count: ' + str(AckCnt)
print 'Total message count: ' + str(TotalCnt)
print 'End.'