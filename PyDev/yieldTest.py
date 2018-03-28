#coding:utf-8

from time import time
import math

start = time()


def primaryfermher(q=2):
    q = abs(q)
    if q == 2: return True
    if q < 2 or q & 1 == 0: return False
    return pow(2,(q-1),q) == 1

def primaryfermher2(q=2,k=100):
    q = abs(q)
    if q == 2: return True
    if q < 2 or q & 1 == 0: return False
    for i in range(3,k):
        x,y = q,i
        while y:
            x,y = y, x % y
        if x != 1: continue
        if pow(i,(q-1),q) != 1:
            return False
    return True
    
def tf():
    
    mylist = range(3)
    for x in mylist:
        yield x * x
    
def elapsed():
    return time() - start
    

def main():

    print '%.3fs: Started: ' % elapsed()    
    iter = tf()
    for i in iter:
        print i
    print '%.3fs: Started: ' % elapsed()
    
    prime = []
    for x in range(2,100000):
        if primaryfermher2(x):
            prime.append(x)
                
    print prime
    
if __name__ == '__main__':
    main()
