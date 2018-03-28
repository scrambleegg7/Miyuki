#coding: utf-8

import sys
import datetime
import re
import readCSVF
from StringClass import StringClass

class kiClass(object):
    
    attributes = ['receiptyNo']
    
    def __init__(self):
        self.clientNo = None
        
    def setData(self,c_no,params):
        try:
            self.clientNo = c_no
        except:
            print " *** Unexpected error: (KI - setData) *** : ", sys.exc_info()[0]
            raise
        
        return True

    def readFile(self,f,skip=True):
        fhd = readCSVF.readFileCSVEXCEL(f,skip)
        return fhd
        
    def inserter(self,param):
       try:
           sqlbase = "insert into ki (receiptyNo) values(%s) "
           setpieces = []
           data_array = {}
        
           for idx, atr in enumerate(self.attributes):
               data_array[atr] = param[idx]
           for atr  in self.attributes:
               setpieces.append("%(" + atr + ")s" )
       
           return sqlbase % ',' .join(setpieces), data_array
       except:
            print " *** Unexpected error (KI - inserter) *** :", sys.exc_info()[0]

    def fieldFormatter(self):
        #print rr[0:6]
        #unicode(rr[3],'KIift-jis').encode('utf-8')
        # change datetime format for mySql
        try:
            params = []
            params.append(self.clientNo)
            return params
        except:
            print "** Unexpected error(KI - fieldFormatter):", sys.exc_info()[0]