#coding: utf-8

import sys
import datetime
import re
import readCSVF

class outgoingClass(object):
    
    
    def __init__(self):
        self.outdate = None
        self.drCode = None
        self.LappingCode = None
        self.standard = None
        self.amount = None
        self.institutionCode = None
        self.institutionName = None
        self.cashAmount = None
        self.drugName = None
        
        self.attributes = ['outdate','drCode','LappingCode','standard','amount','institutionCode','institutionName','cashAmount','drugName']
    


    def inserter(self,param):
       sqlbase = 'insert into outgoing  (outdate,drCode,LappingCode,standard,amount,institutionCode,institutionName,cashAmount,drugName) values ( %s );'
       setpieces = []
       
       data_array = {}
       
       for x,y in enumerate(self.attributes):
           print x,y,param[x]
       
       print "-- inserter : log "
       try:
           for idx,atr in enumerate(self.attributes):
               data_array[atr] = param[idx]
       
           for atr  in self.attributes:
               setpieces.append("%(" + atr + ")s" )

       except:
            print " *** Unexpected error (inserter of outgoingClass - main) *** :", sys.exc_info()[0]

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
        print ymd_date.strftime("%Y-%m-%d")
        
        params = []
        #ymd = datetime.date.today()
        params.append(ymd_date.strftime("%Y-%m-%d"))
        params.append( long(rr[2]) )
        params.append( long(rr[3]) )
        
        params.append(self.numchardetect( rr[4]) )
        params.append( float(rr[6]) )
        params.append( rr[8] )
        params.append(rr[9].decode('cp932'))
        params.append( float(rr[10]) )
        
        # on unicode version, sentence is split out with space (\s+)
        rrsplit = []
        regex2 = re.compile(ur"\s+",re.UNICODE)
        rsplit = regex2.split(rr[11].decode('cp932'))
        params.append(rsplit[0])
    
        return params
       