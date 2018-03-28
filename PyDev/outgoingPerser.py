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
from outgoingClass import outgoingClass
from MyDateClass import MyDateClass

import readCSVF

start = time.time()

def progress():
    return True

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
    
    outgoingObj = outgoingClass()
    myDateObj = MyDateClass()
    YYYYMMDD = myDateObj.strYYYYMMDD()
   
    uStr = u'出庫'
    udirPath = u"\\\\EMSCR01\\ReceptyN\\TEXT\\出庫%s*.csv" % (YYYYMMDD)
    print "-- user directory path for wildcard %s:" % udirPath
    #f = "\\\\EMSCR01\ReceptyN\TEXT\%s%s.CSV" % (uStr.encode('shift-jis') , YYYYMMDD)  
    targets = glob.glob(udirPath)
    if not targets:
        print "-- Files are no longer existed : ---"
        sys.exit()
    
    targets.reverse()
    
    for target in targets:
        print target
    
    f = get_first(targets)
    print "first item of output file : %s" % f
    
    print 'INPUT File Name : %s' % f
    print '%.3fs: Started: ' % elapsed()
    fhd = outgoingObj.readFile(f,True)
    rows_count = list(fhd)
    total_records = len(rows_count)

    print "** Total Records to be inserted: %d" % total_records     
    if fhd is None:
        print "fhd is none."
    else:
        CacheDBObj = CacheDB('receipty')
        #CacheDBObj = CacheDB('receipty','hiromi-EPSONPC')
        try:
            with CacheDBObj:
                #delete exisiting all records
                sqlstat = "delete from outgoing"
                ret_code = CacheDBObj.recordProcessWithSql(sqlstat)
                
                #for rr in fhd:
                for i, rr in enumerate(rows_count):
                    params = outgoingObj.fieldFormatter(rr)
                    #print params
                    
                    data_array = []                    
                    sqlInsertStat, data_array = outgoingObj.inserter(params)
                    #print sqlInsertStat
                    ret_code = CacheDBObj.addRecordSentence(sqlInsertStat, data_array)
                    
                    print "*** Total Records inserted : %d of %d *** " % (i+1, total_records)
                
                #print "Update outgoing with  DrugMaster "
                #sqlstat = "call updateDrugCode()"
                #ret_code = CacheDBObj.recordProcessWithSql(sqlstat)
                
                print '%.3fs: loaded' % elapsed()
                
        except:
            print " *** Unexpected error (receiptyDataLoader - main) *** :", sys.exc_info()[0]
        
if __name__ == '__main__':
    main()
    
    
