#coding: utf-8

import datetime
import time
import MySQLdb
import csv
import numpy as np
import os
import glob
import sys

#from readCSFV import testFunc
from CacheDBClass import CacheDB
from MyDateClass import MyDateClass
import readCSVF

start = time.time()

def get_first(iterable,default=None):
    if iterable:
        for item in iterable:
            return item
    return default


def count(f):
    while 1:
        block = f.read(65536)
        if not block:
             break
        yield block.count(',')

def elapsed():
    return time.time() - start

def main():
    
    argvs = sys.argv
    argc = len(argvs)
    inYY = None
    inMM = None
    
    if (argc != 3):
        print "Usage: ipython %s YY MM (eg. 25 03) " % argvs[0]
        sys.exit()
    else:
        inYY = argvs[1]
        inMM = argvs[2]
    
    print "YEAR (wareki) : %s " % inYY
    print "Month  : %s " % inMM
        
    myDateObj = MyDateClass()
    YYYYMMDD = myDateObj.strYYYYMMDD()
    MM = myDateObj.strMM()

    print '%.3fs: Started: ' % elapsed()    
    CacheDBObj = CacheDB('receipty')
    try:
        with CacheDBObj:
            print "** Call createclientdrug **"
            YYMM = inYY + inMM
            sqlstat = "call createClientDrug(%s) " % YYMM
            ret_code = CacheDBObj.recordProcessWithSql(sqlstat)
            
            sqlstat = "call updateprojection() " 
            ret_code = CacheDBObj.recordProcessWithSql(sqlstat)

            print '%.3fs: loaded' % elapsed()
                
    except:
        print " *** Unexpected error (receiptyDataLoader - main) *** :", sys.exc_info()[0]

if __name__ == '__main__':
    main()
    
    
