#coding: utf-8

import datetime
import time
import MySQLdb
import csv
import glob
import sys
#from readCSFV import testFunc
from CacheDBClass import CacheDB
from dailyClass import dailyClass

import readCSVF

start = time.time()

def progress():
    return True

def count(f):
    while 1:
        block = f.read(65536)
        if not block:
             break
        yield block.count(',')

def elapsed():
    return time.time() - start

def test1():

    f = "\\\\EMSCR01\ReceptyN\TEXT\NIKKEI.TXT"
    targets= glob.glob(f)
    if not targets:
        print "-- Files are no longer existed : "
        sys.exit()
        
    #fhd = dailyObj.readFile(f)
    print "reading : ", f, " ..."
    rf = open(f,"rb")
    dialect = csv.excel
    linecount = sum(count(rf))
    
    fhandler = csv.reader(rf,dialect)
    
    print '\n%.3fs: file has %s rows' % (elapsed(), linecount)

    n = 0
    for row in fhandler:
        n = n + 1
        #print row[0],row[1],row[2],row[3],row[4],row[5]
        #print i
    
    print '%.3fs: loaded' % elapsed()

def main():
    
    dailyObj = dailyClass()
    skip = True
    f = "\\\\EMSCR01\ReceptyN\TEXT\NIKKEI\NIKKEI.TXT"
    fhd = dailyObj.readFile(f,skip)
    print '%.3fs: Started: ' % elapsed()

    n = 0
    if fhd is None:
        print "fhd is none."
    else:
        CacheDBObj = CacheDB('receipty')
        try:
            with CacheDBObj:
                #delete exisiting all records
                ret_code = CacheDBObj.deleteRecord()
                for rr in fhd:
                    n = n + 1 
                    params = dailyObj.fieldFormatter(rr)
            
                    #print params
                    data_array = []                    
                    sqlInsertStat, data_array = dailyObj.inserter(params)
                    ret_code = CacheDBObj.addRecordSentence(sqlInsertStat, data_array)
        
                    print n

                print '%.3fs: loaded' % elapsed()
        except:
            pass
        
if __name__ == '__main__':
    main()
    
    
