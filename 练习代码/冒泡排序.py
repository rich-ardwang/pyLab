import random

def GetInputD(n):
    return random.sample(xrange(n), n)

def SortD(inLst, f):
    s = inLst[:]   #复制列表，如果s=inLst，则s只是inLst的引用
    l = len(s)
    if l > 2:
        b = False
        while b == False:
            b = True
            for i in range(l-1):
                if f == True:
                    if s[i] > s[i+1]:
                        swap(s, i, i+1)
                        b = False
                else:
                    if s[i] < s[i+1]:
                        swap(s, i, i+1)
                        b = False
    return s

def swap(lst, index1, index2):
    tmp = lst[index1]
    lst[index1] = lst[index2]
    lst[index2] =tmp
