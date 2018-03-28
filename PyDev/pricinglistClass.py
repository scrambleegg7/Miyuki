#coding: utf-8

import sys
import datetime
import re
import numpy as np

import readCSVF

from MyDateClass import MyDateClass
from CacheDBClass import CacheDB

class pricinglistClass(object):
    
    attributes = ['jancode','drugName','standard','pricing' \
                  ,'wholeSale','wholeSaleName']
    
    JanCodesPrices = {}
    JanCodesItems = {}
    #items = []

    def __init__(self):
        self.jancode = None
        self.drugName = None
        self.standard = None
        self.pricing = None
        self.wholeSale = None
        self.wholeSaleName = None
        

    def inserter(self,param):
       sqlbase = 'insert into pricinglist (jancode,drugName,standard,pricing,wholeSale,wholeSaleName) values ( %s );'
       setpieces = []
       
       data_array = {}
       idx = 0 
       for atr in self.attributes:
           data_array[atr] = param[idx]
           idx = idx + 1
       
       for atr  in self.attributes:
           setpieces.append("%(" + atr + ")s" )
       
       return sqlbase % ',' .join(setpieces), data_array

    def deployments(self,params):
        """
         0  ,    1        2           3      4        5           6           7       8      9
        indate,drCode,LappingCode,standard,amount,wholeSale,wholeSaleName,jancode,payment,drugName
        """
        if params[7] not in self.JanCodesPrices:
            items = []
            items.append(params[9]) #drugname
            items.append(params[3]) # standard
            items.append(params[6]) # wholesaleName
            self.JanCodesItems[params[7]] = items 
            
            wholes = {}
            wholes[params[5]] = [params[6],params[8]] # wholesale : wholesalename & payment 
            self.JanCodesPrices[params[7]] =  wholes
        else:
            wholes = self.JanCodesPrices[params[7]]
            for k,v in wholes.iteritems():
                #if params[7] == 4987087031126: 
                    #pass
                    #print k,v, params[8] 
                if v[1] > params[8]:
                    newwholes = {}
                    newwholes[params[5]] = [params[6],params[8]] # wholesale : wholesalename & payment 
                    self.JanCodesPrices[params[7]] =  newwholes
                    #print self.JanCodesPrices[params[7]]
                    #if params[7] == 4987087031126: 
                        #print newwholes
                        #print self.JanCodesPrices

                    
    def listingDataInsert(self,DBObj):
        
        #print self.JanCodesPrices
        #print self.JanCodesItems
        for jancode,v in self.JanCodesPrices.iteritems():
            for k1,v1 in v.iteritems():
                wholeSale = k1
                wholeSalename = v1[0]
                price = v1[1]
                
            items = self.JanCodesItems[jancode]
            drugname = items[0]
            standard = items[1]
            #wholeSalename = items[2] 
            """
            no need to decode or encode into cp932 / utf8
            """
            params = []
            params.append(jancode)
            params.append(drugname)
            params.append(standard)
            params.append(float(price))
            params.append(wholeSale)
            params.append(wholeSalename)

            sqlInsertStat, data_array = self.inserter(params)
            ret_code = DBObj.addRecordSentence(sqlInsertStat, data_array)
    
    def deleteRecordSQL(self):
        sqlbase = 'delete from pricinglist'
        return sqlbase

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
            #return data.decode('utf-8')


    def dataSelectSQL1(self):
        #print "dataSelect1"
        dateObj = MyDateClass()
        sqlstat = 'select jancode,drugName,standard,pricing,wholeSale,wholeSaleName from expectation \
                   where issuedate >= \'%s\' and drugClarify = \'%s\' order by drugName, issueDate'
        print sqlstat % (t,dg)
        return sqlstat % (t,dg)



    def fieldFormatter(self,rr):
        """
        table to table --> need to encode utf8
        csv to table --> need to encode cp932  
        """
        #print rr
        params = []
        params.append(rr[0])
        params.append(rr[1].encode('cp932'))
        params.append(self.numchardetect(rr[2]))
        #params.append(rr[3])
        params.append(rr[3])
        params.append(rr[4])
        params.append(rr[5].encode('cp932'))
        
        return params

