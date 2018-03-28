#coding: utf-8

import sys
import datetime
import re
import numpy as np

import readCSVF

from MyDateClass import MyDateClass
from CacheDBClass import CacheDB
#from pyGammaClass import pyGammaClass

class forwardClientClass(object):
    
    attributes = ['nextIssueDate','clientName','totalAmount','drugName' \
                  ,'stockAmount','mu','std','msg1','msg2']
    
    def __init__(self):
        self.nextIssueDate = None
        self.clientName = None
        self.totalamount = None
        self.drugName = None
        self.stockName = None
        self.mu = None
        self.msg1 = None
        self.msg2 = None

    def inserter(self,param):
       sqlbase = 'insert into forwardClient (nextIssueDate,clientName,totalAmount,drugName,stockAmount,mu,std,msg1,msg2) values ( %s );'
       setpieces = []
       
       data_array = {}
       idx = 0 
       for atr in self.attributes:
           data_array[atr] = param[idx]
           idx = idx + 1
       
       for atr  in self.attributes:
           setpieces.append("%(" + atr + ")s" )
       
       return sqlbase % ',' .join(setpieces), data_array

    def readFile(self,f,skip=True):
        fhd = readCSVF.readFileCSVEXCEL(f,skip)
        return fhd

    def chardetect(self,data):
        encodings = ('cp932')
        for enc in encodings:
            try:
                data.decode(enc,errors='ignore')
            except UnicodeError:
                continue
            return enc
        return False
    
    def numchardetect(self,data):
        regexp = re.compile(r'^[0-9A-Za-z]+$')
        result = regexp.search(data)
        if result != None:
            #print "-- num char only"
            return data
        else:
            #print "-- Non num char "
            return data.decode('cp932')

    def fieldFormatter(self,rr):
        """
        table to table --> need to encode utf8
        csv to table --> need to encode cp932  
        """
        params = []
        params.append(rr[0].strftime("%Y-%m-%d"))
        params.append(rr[1].encode('utf-8'))
        #params.append(rr[1])
        params.append(rr[2])
        params.append(rr[3].encode('utf-8'))
        #params.append(rr[3])
        params.append(rr[4])
        params.append(rr[5])
        params.append(rr[6])
        params.append(rr[7])
        params.append(rr[8])
    
        return params

