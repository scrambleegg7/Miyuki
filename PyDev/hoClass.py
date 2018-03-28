#coding: utf-8

import sys
import datetime
import re
import readCSVF
from StringClass import StringClass

class hoClass(object):
    
    attributes = ['receiptyNo','insuranceNo','insuranceKigo','insuranceBango']
    
    def __init__(self):
        self.clientNo = None
        self.insuranceNo = None
        self.insuranceKigo = None
        self.insuranceBango = None
        
    def setData(self,codes,params):
        try:
            self.clientNo = codes
            self.insuranceNo = params[1]
            self.insuranceKigo = StringClass(params[2])
            self.insuranceBango = StringClass(params[3])
            
        except:
            print " *** Unexpected error: (HO - setData) *** : ", sys.exc_info()[0]
            raise
        
        return True

    def readFile(self,f,skip=True):
        fhd = readCSVF.readFileCSVEXCEL(f,skip)
        return fhd

        
    def inserter(self,param):
       try:
           sqlbase = "insert into ho (receiptyNo,insuranceNo,insuranceKigo,insuranceBango) values(%s) "
           setpieces = []
           data_array = {}
        
           for idx, atr in enumerate(self.attributes):
               data_array[atr] = param[idx]
           for atr  in self.attributes:
               setpieces.append("%(" + atr + ")s" )
       
           return sqlbase % ',' .join(setpieces), data_array
       except:
            print " *** Unexpected error (HO - inserter) *** :", sys.exc_info()[0]


    def fieldFormatter(self):
        #print rr[0:6]
        #unicode(rr[3],'HOift-jis').encode('utf-8')
        # change datetime format for mySql
        try:
            params = []
            params.append(self.clientNo)
            params.append(self.insuranceNo)
            params.append(self.insuranceKigo.cp932Converter())
            params.append(self.insuranceBango.cp932Converter())
            
            return params
        except:
            print "** Unexpected error(HO - fieldFormatter):", sys.exc_info()[0]