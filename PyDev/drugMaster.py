#coding: utf-8

import datetime
import time
import MySQLdb
import csv
import numpy as np
#from readCSFV import testFunc
from CacheDBClass import CacheDB
from drugMasterClass import drugMasterClass
from MyDateClass import MyDateClass

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

def main():
    
    drugMasterObj = drugMasterClass()
    myDateObj = MyDateClass()
    YYYYMMDD = myDateObj.strYYYYMMDD()
   
    uStr = u'管理データ'
    
    f = "F:\\myCompany\\hiromi\\Documents\\EM-%s\\y.CSV" % uStr.encode('shift-jis')  
    print 'INPUT File Name : %s' % f
    print '%.3fs: Started: ' % elapsed()
    fhd = drugMasterObj.readFile(f,True)
    rows_count = list(fhd)
    total_records = len(rows_count)
    
    if fhd is None:
        print "fhd is none."
    else:
        CacheDBObj = CacheDB('receipty')
        try:
            with CacheDBObj:
                #delete exisiting all records
                sqlstat = "delete from DrugMaster"
                ret_code = CacheDBObj.recordProcessWithSql(sqlstat)
                
                #for rr in fhd:
                for i, rr in enumerate(rows_count):
                    params = drugMasterObj.fieldFormatter(rr)

                    data_array = []                    
                    sqlInsertStat, data_array = drugMasterObj.inserter(params)
                    ret_code = CacheDBObj.addRecordSentence(sqlInsertStat, data_array)
                    
                    #print "Total Records inserted : %d of %d " % (i+1, total_records)
                
                print "Update StockMaster with  DrugMaster "
                sqlstat = "call updateDrugCode()"
                ret_code = CacheDBObj.recordProcessWithSql(sqlstat)
                
                print '%.3fs: loaded' % elapsed()

                pass
                
        except:
            pass
        
if __name__ == '__main__':
    main()
    
    
