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
from reClass import reClass
from shClass import shClass
from koClass import koClass
from kiClass import kiClass
from iyClass import iyClass
from hoClass import hoClass
from czClass import czClass
from tkClass import tkClass
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
        
    reObj = reClass()
    myDateObj = MyDateClass()
    YYYYMMDD = myDateObj.strYYYYMMDD()
    MM = myDateObj.strMM()

    ufileName = "RECEIPTY.CYO";
    n2Bytes_uni = u'国保'
    s2Bytes_uni = u'社保'
    infiles = []
    k_infile_this = "L:\\RECEPTY\\national\\%s" % ufileName
    s_infile_this = "L:\\RECEPTY\\tokyo\\%s" % ufileName
    if inMM == MM:
        infiles.append(k_infile_this)
        infiles.append(s_infile_this)
        print k_infile_this
        print s_infile_this
    else:
        
        k_infile = 'F:\\Recepty\\EMData\\%s\\%d\\%s' % (n2Bytes_uni,int(inMM),ufileName)  
        s_infile = 'F:\\Recepty\\EMData\\%s\\%d\\%s' % (s2Bytes_uni,int(inMM),ufileName) 
        infiles.append(k_infile)
        infiles.append(s_infile)

        print k_infile
        print s_infile
        #sys.exit(0)
        

    flags = ['national', 'tokyo']
    #uStr = u'出庫'
    print '%.3fs: Started: ' % elapsed()    
    CacheDBObj = CacheDB('receipty')
    try:
        with CacheDBObj:
            print "delete exisiting all records from expecation"
            YYMM = inYY + inMM
            sqlstat = "call deleteAllReceipty(%s) " % YYMM
            ret_code = CacheDBObj.recordProcessWithSql(sqlstat)
            
            for fileIndex, f in enumerate(infiles):
                fhd = reObj.readFile(f,True)
                rows_count = list(fhd)
                total_records = len(rows_count)

                print " --> File Index : %s" % fileIndex
                print "RE : %s records" %  sum([1 for r in rows_count if r[0] == 'RE'])
                print "SH : %s records" %  sum([1 for r in rows_count if r[0] == 'SH'])
                print "KO : %s records" %  sum([1 for r in rows_count if r[0] == 'KO'])
                print "KI : %s records" %  sum([1 for r in rows_count if r[0] == 'KI'])
                print "IY : %s records" %  sum([1 for r in rows_count if r[0] == 'IY'])
                print "HO : %s records" %  sum([1 for r in rows_count if r[0] == 'HO'])
                print "CZ : %s records" %  sum([1 for r in rows_count if r[0] == 'CZ'])
                print "TK : %s records" %  sum([1 for r in rows_count if r[0] == 'TK'])

                print 'INPUT File Name : %s' % f
                clientNo = None
                shNo = None
                doctorCode = None

                for i, rr in enumerate(rows_count):
                    """
                    RE record 
                    """
                    ##print rr
                    data_array = []
                    params = []
                    if rr[0] == "RE":
                        #print " -- call setData (RE) -- "
                        ret_code = reObj.setData(fileIndex,rr)
                        params = reObj.fieldFormatter()                    
                        sqlInsertStat, data_array = reObj.inserter(params)
                    
                    clientNo = reObj.getClientNo()
                    #
                    if rr[0] == "SH":
                        shObj = shClass()
                        ret_code = shObj.setData(clientNo,rr)
                        params = shObj.fieldFormatter()                    
                        sqlInsertStat, data_array = shObj.inserter(params)                    
                        shNo = shObj.getshNo()
                    #
                    if rr[0] == "HO":
                        hoObj = hoClass()
                        ret_code = hoObj.setData(clientNo,rr)
                        params = hoObj.fieldFormatter()                    
                        sqlInsertStat, data_array = hoObj.inserter(params)                    
                    #
                    if rr[0] == "KO":
                        koObj = koClass()
                        ret_code = koObj.setData(clientNo,rr)
                        params = koObj.fieldFormatter()                    
                        sqlInsertStat, data_array = koObj.inserter(params)                    

                    if rr[0] == "KI":
                        kiObj = kiClass()
                        ret_code = kiObj.setData(clientNo,rr)
                        params = kiObj.fieldFormatter()                    
                        sqlInsertStat, data_array = kiObj.inserter(params)                    
                    
                    if rr[0] == "CZ":
                        czObj = czClass()
                        codes = []
                        codes.append(clientNo)
                        codes.append(shNo)
                        ret_code = czObj.setData(codes,rr)
                        params = czObj.fieldFormatter()                    
                        sqlInsertStat, data_array = czObj.inserter(params)                    
                        doctorCode = czObj.getDoctorCode()
                    #print doctorCode
                    
                    if rr[0] == "IY":
                        iyObj = iyClass()
                        codes = []
                        codes.append(clientNo)
                        codes.append(shNo)
                        codes.append(doctorCode)
                        ret_code = iyObj.setData(codes,rr)
                        params = iyObj.fieldFormatter()                    
                        sqlInsertStat, data_array = iyObj.inserter(params)                    

                    if rr[0] == "TK":
                        tkObj = tkClass()
                        ret_code = tkObj.setData(clientNo,rr)
                        params = tkObj.fieldFormatter()                    
                        sqlInsertStat, data_array = tkObj.inserter(params)                    
                    ##if rr[0] == "RE" or rr[0] == "SH" or rr[0] == "HO" or rr[0] == "KO" or rr[0] == "KI" or rr[0] == "IY" or rr[0] == "CZ": 
                    if rr[0] == "RE" or rr[0] == "SH" or rr[0] == "CZ" or rr[0] == "IY" or rr[0] == "TK" or rr[0] == "HO" or rr[0] == "KO" or rr[0] == "KI": 
                        ret_code = CacheDBObj.addRecordSentence(sqlInsertStat, data_array)
                    
                    #print "Total Records inserted : %d of %d " % (i+1, total_records)
                
                #print "Update re with  DrugMaster "
                #sqlstat = "call updateDrugCode()"
                #ret_code = CacheDBObj.recordProcessWithSql(sqlstat)
                
                print '%.3fs: loaded' % elapsed()

                pass
                
    except:
        print " *** Unexpected error (receiptyDataLoader - main) *** :", sys.exc_info()[0]

if __name__ == '__main__':
    main()
    
    
