#coding: utf-8

import sys
import datetime
import re
import readCSVF

class incomingClass(object):
    
    attributes = ['indate','drCode','LappingCode','standard','amount','wholeSale','wholeSaleName','jancode','payment','drugName']
    
    def __init__(self):
        self.indate = None
        self.drCode = None
        self.LappingCode = None
        self.standard = None
        self.amount = None
        self.wholeSale = None
        self.wholeSaleName = None
        self.jancode = None
        self.payment = None
        self.drugName = None

    def inserter(self,param):
       sqlbase = 'insert into incoming  (indate,drCode,LappingCode,standard,amount,wholeSale,wholeSaleName,jancode,payment,drugName) values ( %s );'
       setpieces = []
       
       data_array = {}
       #idx = 0 
       for idx,atr in enumerate(self.attributes):
           data_array[atr] = param[idx]
           #idx = idx + 1
       
       #print data_array
       
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
        #print rr[0:6]
        #unicode(rr[3],'shift-jis').encode('utf-8')
        # change datetime format for mySql
        ymd = rr[1].split('/')
        ymd_date = datetime.date(int(ymd[0]),int(ymd[1]),int(ymd[2]))
        #print ymd_date.strftime("%Y-%m-%d")
        
        params = []
        #ymd = datetime.date.today()
        params.append(ymd_date.strftime("%Y-%m-%d"))
        params.append( long(rr[2]) )
        params.append( long(rr[3]) )
        
        params.append(self.numchardetect( rr[4]) )
        params.append( float(rr[6]) )
        params.append( rr[8] )
        params.append(rr[9].decode('cp932'))
        params.append( long(rr[10]) )
        params.append( float(rr[11]) )
        
        # on unicode version, sentence is split out with space (\s+)
        rrsplit = []
        regex2 = re.compile(ur"\s+",re.UNICODE)
        rsplit = regex2.split(rr[12].decode('cp932'))
        params.append(rsplit[0])
    
        return params
       