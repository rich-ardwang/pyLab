# -*- coding: cp936 -*-
s='abcdefghijklmnopqrstuvwxyz'
for i in range(len(s),0,-1):
    print s[:i]

#���߲�������ķ���
for i in [None] + range(-1,-len(s),-1):
    print s[:i]
