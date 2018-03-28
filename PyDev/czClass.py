#coding: utf-8

import sys
import datetime
import re
import readCSVF
from StringClass import StringClass

class czClass(object):
    
    attributes = ['receiptyNo','shNo','doctorCode','shDate','czDate','czCount','czDays']
    
    def __init__(self):
        self.clientNo = None
        self.shNo = None
        self.doctorCode = None
        self.shDate = None
        self.czDate = None
        self.czCount = None
        self.czDays = None
        
    def setData(self,codes,params):
        try:
            self.clientNo = codes[0]
            self.shNo = codes[1]
            self.doctorCode = params[1]
            self.shDate = params[2]
            self.czDate = params[3]
            self.czCount = params[4]
            self.czDays = params[5]
            
        except:
            print " *** Unexpected error: (CZ - setData) *** : ", sys.exc_info()[0]
            raise
        
        return True

    def readFile(self,f,skip=True):
        fhd = readCSVF.readFileCSVEXCEL(f,skip)
        return fhd

    def getDoctorCode(self):
        return self.doctorCode
        
    def inserter(self,param):
       try:
           sqlbase = "insert into cz (receiptyNo,shNo,doctorCode,shDate,czDate,czCount,czDays) values(%s) "
           setpieces = []
           data_array = {}
        
           for idx, atr in enumerate(self.attributes):
               data_array[atr] = param[idx]
           for atr  in self.attributes:
               setpieces.append("%(" + atr + ")s" )
       
           return sqlbase % ',' .join(setpieces), data_array
       except:
            print " *** Unexpected error (CZ - inserter) *** :", sys.exc_info()[0]

    def fieldFormatter(self):
        #print rr[0:6]
        #unicode(rr[3],'CZift-jis').encode('utf-8')
        # change datetime format for mySql
        try:
            params = []
            params.append(self.clientNo)
            params.append(self.shNo)
            params.append(int(self.doctorCode))
            params.append(self.shDate)
            params.append(self.czDate)
            params.append(int(self.czCount))
            params.append(int(self.czDays))
            
            return params
        except:
            print "Unexpected error(CZ - fieldFormatter):", sys.exc_info()[0]