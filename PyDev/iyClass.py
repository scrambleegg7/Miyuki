#coding: utf-8

import sys
import datetime
import re
import readCSVF
from StringClass import StringClass

class iyClass(object):
    
    attributes = ['receiptyNo','shNo','doctorCode','drugCode','drugAmount']
    
    def __init__(self):
        self.clientNo = None
        self.shNo = None
        self.doctorCode = None
        self.drugCode = None
        self.drugAmount = None
        
    def setData(self,codes,params):
        try:
            self.clientNo = codes[0]
            self.shNo = codes[1]
            self.doctorCode = codes[2]
            self.drugCode = params[2]
            self.drugAmount = params[3]
            
        except:
            print " *** Unexpected error: (IY - setData) *** : ", sys.exc_info()[0]
            raise
        
        return True

    def readFile(self,f,skip=True):
        fhd = readCSVF.readFileCSVEXCEL(f,skip)
        return fhd

        
    def inserter(self,param):
       try:
           sqlbase = "insert into iy (receiptyNo,shNo,doctorCode,drugCode,drugAmount) values(%s) "
           setpieces = []
           data_array = {}
        
           for idx, atr in enumerate(self.attributes):
               data_array[atr] = param[idx]
           for atr  in self.attributes:
               setpieces.append("%(" + atr + ")s" )
       
           return sqlbase % ',' .join(setpieces), data_array
       except:
            print " *** Unexpected error (IY - inserter) *** :", sys.exc_info()[0]


    def fieldFormatter(self):
        #print rr[0:6]
        #unicode(rr[3],'IYift-jis').encode('utf-8')
        # change datetime format for mySql
        try:
            params = []
            params.append(self.clientNo)
            params.append(int(self.shNo))
            params.append(int(self.doctorCode))
            params.append(int(self.drugCode))
            params.append(float(self.drugAmount))
            
            return params
        except:
            print "Unexpected error(IY - fieldFormatter):", sys.exc_info()[0]