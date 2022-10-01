import urllib.request
import os
import json
import uuid
from time import sleep
import base64
import socket
import time

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
        val = int.from_bytes(f.read(4), byteorder='little')
        self.year = val & 4095
        self.month = (val >> 12) & 15
        self.day = (val >> 16) & 31
        self.hour = (val >> 21) & 31
        self.min = (val >> 26) & 63
        val = int.from_bytes(f.read(4), byteorder='little')
        self.sec = val & 63
        self.usec = (val >> 6) & 1048575
        self.res = (val >> 26) & 63

    def __str__(self):
        return "%04d-%02d-%02d %02d:%02d:%02d"%(self.year,self.month,self.day,self.hour,self.min,self.sec)

chatMap = {}
class chatItem:
    def __init__(self):
        self.uid = 0
        self.fileno = 0
        self.msglen = 0
        self.startpos = 0
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.min = 0
        self.sec = 0
        self.usec = 0
        self.res = 0
        self.oriSender = 0
        self.seqID = 0
        self.l = 0
        self.r = 0
        self.chatType = 0

    def parseFromFile(self,f):
        self.uid = int.from_bytes(f.read(8), byteorder='little')
        self.fileno = int.from_bytes(f.read(4), byteorder='little')
        self.msglen = int.from_bytes(f.read(4), byteorder='little')
        self.startpos = int.from_bytes(f.read(4), byteorder='little')
        val = int.from_bytes(f.read(4), byteorder='little')
        self.year = val & 4095
        self.month = (val >> 12) & 15
        self.day = (val >> 16) & 31
        self.hour = (val >> 21) & 31
        self.min = (val >> 26) & 63
        val = int.from_bytes(f.read(4), byteorder='little')
        self.sec = val & 63
        self.usec = (val >> 6) & 1048575
        self.res = (val >> 26) & 63

        self.oriSender = int.from_bytes(f.read(4), byteorder='little')
        self.seqID = int.from_bytes(f.read(4), byteorder='little')

        self.l = self.uid >> 32
        self.r = self.uid & 0xffffffff
        if self.l!=0:
            self.chatType = 1
        elif self.r!=self.oriSender:
            self.chatType = 2


class ChatMsgInfo:
    def __init__(self):
        self.tag = 0
        self.type = 0
        self.valid = 0
        self.len = 0
        self.msgtag = ""
        self.chattype = 0
        self.sendtime = chatTime()
        self.senduserid = 0
        self.receivers = []
        self.chatmessage = ""
        self.ackflag = 0
        self.acktime = chatTime()
        self.tailtag = 0

    def getpicFromNetDisk(self,pictag,senduserid,recvuserid):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("180.96.8.52", 80))
        # s.connect(("10.202.16.12", 16888))

        totallen = 10+2+len(pictag)+4+4
        buf = bytearray()
        buf.append(0x77)
        buf.extend(totallen.to_bytes(4,byteorder='big'))
        buf.extend((1019).to_bytes(2,byteorder='big'))
        buf.extend((0x00).to_bytes(2, byteorder='big'))
        buf.append(0x00)

        buf.extend(len(pictag).to_bytes(2, byteorder='big'))
        buf.extend(pictag.encode())
        buf.extend(senduserid.to_bytes(4, byteorder='big'))
        buf.extend(recvuserid.to_bytes(4, byteorder='big'))

        s.send(buf)
        data = s.recv(1024)
        filelength = 0
        if len(data) > 12:
            retcode = int.from_bytes(data[10:12], byteorder='big')
            if retcode!=0:
                return False
            else:
                retmsglen = int.from_bytes(data[12:14], byteorder='big')
                filenamelen = int.from_bytes(data[14+retmsglen:14+retmsglen+2], byteorder='big')
                filename = data[14+retmsglen+2:14+retmsglen+2+filenamelen].decode()
                filelength = int.from_bytes(data[14+retmsglen+2+filenamelen:14+retmsglen+2+filenamelen+4], byteorder='big')

        totallen = 2+4+2 + 2 + len(pictag) + 4 + 4
        buf = bytearray()
        buf.append(0x77)
        buf.extend(totallen.to_bytes(4, byteorder='big'))
        buf.extend((1017).to_bytes(2, byteorder='big'))
        buf.extend(len(pictag).to_bytes(2, byteorder='big'))
        buf.extend(pictag.encode())
        buf.append(0x00)
        
        buf.extend((0x00).to_bytes(4, byteorder='big'))
        buf.extend((filelength).to_bytes(4, byteorder='big'))

        s.send(buf)
        data = s.recv(1024)

        if len(data) > 12:
            retcode = int.from_bytes(data[10:12], byteorder='big')
            if retcode != 0:
                return False
            else:
                retmsglen = int.from_bytes(data[12:14], byteorder='big')

        readlen = 0
        filebuf = bytearray()
        while True:
            try:
                data = s.recv(10240)
                filebuf.extend(data)
                readlen += len(data)
                if readlen>=filelength:
                    break
            except:
                return False
        with open('./chat/'+pictag+'.jpg',"wb") as f:
            f.write(filebuf)
            return True


    def decodeChatMessage(self,message):
        msgs = []
        try:
            msgs = message.split('|')
            if len(msgs)<3:
                return ""
            if msgs[1]=='0':
                return base64.b64decode(msgs[2]).decode()
            elif msgs[1]=='1' and len(msgs)>=7 and len(self.receivers)>0:
                pictag = base64.b64decode(msgs[6]).decode()
                # self.getpicFromNetDisk(pictag,self.senduserid,self.receivers[0])
                return pictag
            else:
                return msgs[1]
        except:
            return ""

    def parseFromFile(self, f):
        # msg header 8 bytes
        self.tag = int.from_bytes(f.read(2), byteorder='little')
        self.type = int.from_bytes(f.read(1), byteorder='little')
        self.valid = int.from_bytes(f.read(1), byteorder='little')
        self.len = int.from_bytes(f.read(4), byteorder='little')
        if self.type != 0x43:  # 'C'
            f.read(self.len-8)
            return False

        if self.tag != 0x7F15:
            f.read(self.len-8)
            return False
        # msg tag
        taglen = int.from_bytes(f.read(2), byteorder='little')
        self.msgtag = f.read(taglen).decode()
        self.chattype = int.from_bytes(f.read(1), byteorder='little')
        self.sendtime.parseFromFile(f)
        self.senduserid = int.from_bytes(f.read(4), byteorder='little')

        # recvs
        recvcount = int.from_bytes(f.read(2), byteorder='little')
        for j in range(recvcount):
            self.receivers.append(int.from_bytes(f.read(4), byteorder='little'))
        # msg
        msglen = int.from_bytes(f.read(4), byteorder='little')
        self.chatmessage = self.decodeChatMessage(f.read(msglen).decode())

        self.ackflag = int.from_bytes(f.read(1), byteorder='little')
        self.acktime.parseFromFile(f)

        self.tailtag = int.from_bytes(f.read(2), byteorder='little')
        if self.tailtag != 0x1FF1:
            return False
        return True

def parseChatFile(chatfile):
    with  open(chatfile,"rb") as f:
        magicnumber = int.from_bytes(f.read(4),byteorder='little')
        count = int.from_bytes(f.read(4),byteorder='little')

        for i in range(count):
            item = chatItem()
            item.parseFromFile(f)
            if item.l!=0:
                chatMap.setdefault(item.l,[])
                chatMap[item.l].append(item)
            elif item.r!=item.oriSender and item.oriSender!=0:
                chatMap.setdefault(item.oriSender, [])
                chatMap[item.oriSender].append(item)

def parseMsgFromIdx(idxMap,chatinfodb):
    starttime = time.time()
    with  open(chatinfodb, "rb") as f:
        # read DBFile header
        dbtype = f.read(1)
        version = f.read(1)
        byteorder = f.read(1)
        headertag = f.read(13)
        fileheadcrc = int.from_bytes(f.read(4), byteorder='little')
        filecrc = int.from_bytes(f.read(4), byteorder='little')
        dbsize = int.from_bytes(f.read(4), byteorder='little')
        reserve = f.read(4)
        dataoffset = int.from_bytes(f.read(4), byteorder='little')
        datasize = int.from_bytes(f.read(4), byteorder='little')
        datawritepos = int.from_bytes(f.read(4), byteorder='little')
        recordcount = int.from_bytes(f.read(4), byteorder='little')

        # load message
        totalcount = 0
        for i in range(recordcount):
            msg = ChatMsgInfo()
            if msg.parseFromFile(f)==False:
                break
            sendtimestr = str(msg.sendtime)
            chatMap.setdefault(msg.senduserid, [])
            chatMap[msg.senduserid].append(msg)
    print("end: %f"%(time.time()-starttime))


if __name__=='__main__':
    # parseChatFile("./chat/20171102.idx")

    parseMsgFromIdx(chatMap,"./20180420_00_ChatInfo")
    a = 1