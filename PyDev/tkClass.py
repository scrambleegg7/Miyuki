#coding: utf-8

import sys
import datetime
import re
import readCSVF
from StringClass import StringClass

class tkClass(object):
    
    attributes = ['receiptyNo','commentCode','charData']
    
    def __init__(self):
        self.clientNo = None
        self.commentCode = None
        self.charData = None
        
    def setData(self,codes,params):
        try:
            self.clientNo = codes
            self.commentCode = params[1]
            self.charData = StringClass(params[2])
        except:
            print " *** Unexpected error: (TK - setData) *** : ", sys.exc_info()[0]
            raise
        
        return True

    def readFile(self,f,skip=True):
        fhd = readCSVF.readFileCSVEXCEL(f,skip)
        return fhd
        
    def inserter(self,param):
       try:
           sqlbase = "insert into tk (receiptyNo,commentCode,charData) values(%s) "
           setpieces = []
           data_array = {}
        
           for idx, atr in enumerate(self.attributes):
               data_array[atr] = param[idx]
           for atr  in self.attributes:
               setpieces.append("%(" + atr + ")s" )
       
           return sqlbase % ',' .join(setpieces), data_array
       except:
            print " *** Unexpected error (TK - inserter) *** :", sys.exc_info()[0]

    def fieldFormatter(self):
        #print rr[0:6]
        #unicode(rr[3],'TKift-jis').encode('utf-8')
        # change datetime format for mySql
        try:
            params = []
            params.append(self.clientNo)
            params.append(int(self.commentCode))
            params.append(self.charData.cp932Converter())
            
            return params
        except:
            print "Unexpected error(TK - fieldFormatter):", sys.exc_info()[0]