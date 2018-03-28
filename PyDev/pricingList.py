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
from incomingClass import incomingClass
from MyDateClass import MyDateClass
from pricinglistClass import pricinglistClass
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
    
    incomingObj = incomingClass()
    pricinglistObj = pricinglistClass()
    myDateObj = MyDateClass()
    YYYYMMDD = myDateObj.strYYYYMMDD()
   
    uStr = u'入庫'
    udirPath = u"\\\\EMSCR01\\ReceptyN\\TEXT\\入庫%s*.csv" % (YYYYMMDD)
    print "-- user directory path for wildcard %s:" % udirPath
    #f = "\\\\EMSCR01\ReceptyN\TEXT\%s%s.CSV" % (uStr.encode('shift-jis') , YYYYMMDD)  
    targets = []
    targets = glob.glob(udirPath)
    if not targets:
        print "File is no longer existed : "
        sys.exit()
        
    targets.reverse()
    
    for target in targets:
        print target
    
    f = get_first(targets)
    print "first item of output file : %s" % f
    
    print 'INPUT File Name : %s' % f
    print '%.3fs: Started: ' % elapsed()
    fhd = incomingObj.readFile(f,True)
    rows_count = list(fhd)
    total_records = len(rows_count)
    
    if fhd is None:
        print "fhd is none."
    else:
        CacheDBObj = CacheDB('receipty')
        try:
            with CacheDBObj:
                #delete exisiting all records
                print "delete from pricinglist ...."
                sqlstat = "delete from pricinglist"
                ret_code = CacheDBObj.recordProcessWithSql(sqlstat)
                
                #for rr in fhd:
                
                for i, rr in enumerate(rows_count):
                    if not rr[10] or float(rr[11]) < 0:
                        continue
                        """
                        accept normal wholesale code (> 100 exceptional)
                        """
                    params = incomingObj.fieldFormatter(rr)
                    pricinglistObj.deployments(params)
                    #print "Total Records inserted : %d of %d " % (i+1, total_records)
                
                pricinglistObj.listingDataInsert(CacheDBObj)
                #print "Update incoming with  DrugMaster "
                #sqlstat = "call updateDrugCode()"
                #ret_code = CacheDBObj.recordProcessWithSql(sqlstat)
                
                print '%.3fs: loaded' % elapsed()

                pass
                
        except:
        # エラーの情報をsysモジュールから取得
            info = sys.exc_info()
        # tracebackモジュールのformat_tbメソッドで特定の書式に変換
            tbinfo = traceback.format_tb( info[2] )
        # 収集した情報を読みやすいように整形して出力する----------------------------
            print 'Python Error.'.ljust( 80, '=' )
            for tbi in tbinfo:
                print tbi
            print '  %s' % str( info[1] )
            print '\n'.rjust( 80, '=' )
        

        
if __name__ == '__main__':
    main()
    
    
