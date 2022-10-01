import hashlib
import time
import multiprocessing
import os


shaCnt=1000000
threadCnt=10


#lock=multiprocessing.Lock()

def S256Cnt(x):
    #lock.acquire()
    for n in range(x):
        hashlib.sha256("Hello").hexdigest()
        n=n+1
        #print n
    #lock.release()


def Otox(x):
    return x*x

if __name__ == '__main__':
    lst=[]
    for n in range(threadCnt):
        lst.append(shaCnt/threadCnt)
    print lst
    pool=multiprocessing.Pool(processes=threadCnt)
    t_start=time.time()
    pool.map(S256Cnt, lst)
    t_end=time.time()
    print t_end-t_start