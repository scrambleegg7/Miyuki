#coding: utf-8

import sys
import datetime
import re
import readCSVF
from StringClass import StringClass

class shClass(object):
    
    attributes = ['receiptyNo','shNo','zaikeiCode']
    
    def __init__(self):
        self.clientNo = None
        self.shNo = None
        self.zaikeiCode = None
        
    def setData(self,c_no,params):
        try:
            self.clientNo = c_no
            self.shNo = params[1]
            self.zaikeiCode = params[2]
        except:
            print " *** Unexpected error: (SH - setData) *** : ", sys.exc_info()[0]
            raise
        
        return True

    def readFile(self,f,skip=True):
        fhd = readCSVF.readFileCSVEXCEL(f,skip)
        return fhd

    def getshNo(self):
        return self.shNo
        
    def inserter(self,param):
       try:
           sqlbase = "insert into sh (receiptyNo,shNo,zaikeiCode) values(%s) "
           setpieces = []
           data_array = {}
        
           for idx, atr in enumerate(self.attributes):
               data_array[atr] = param[idx]
           for atr  in self.attributes:
               setpieces.append("%(" + atr + ")s" )
       
           return sqlbase % ',' .join(setpieces), data_array
       except:
            print " *** Unexpected error (SH - inserter) *** :", sys.exc_info()[0]


    def fieldFormatter(self):
        #print rr[0:6]
        #unicode(rr[3],'shift-jis').encode('utf-8')
        # change datetime format for mySql
        try:
            params = []
            params.append(self.clientNo)
            params.append(int(self.shNo))
            params.append(int(self.zaikeiCode))
            return params
        except:
            print "** Unexpected error(SH - fieldFormatter):", sys.exc_info()[0]