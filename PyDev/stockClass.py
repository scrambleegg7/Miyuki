#coding: utf-8

import sys
import datetime
import re
import readCSVF
from MyDateClass import MyDateClass
from CacheDBClass import CacheDB
from pyGammaClass import pyGammaClass

class expectationClass(object):
    
    attributes = ['receiptyNo','chodate','clientName','institution','doctorName','issueDate','days','amount','nextIssueDate','drugCode','drugName' \
                  'totalAmount','drugClarify','projectAmout','undeliverAmount','stockFlag','tobeCome','officialPrice','marketPrice','duration']
    
    def __init__(self):
        self.receiptyNo = None
        self.chodate = None
        self.clientName = None
        self.institution = None
        self.doctorName = None
        self.issueDate = None
        self.days = None
        self.amount = None
        self.nextIssueDate = None
        self.drugCode = None

    def inserter(self,param):
       sqlbase = 'insert into expectation  (receiptyNo,chodate,clientName,institution,doctorName,issueDate,days,amount,nextIssueDate,drugCode,drugName \
                      totalAmount,drugClarify,projectAmout,undeliverAmount,stockFlag,tobeCome,officialPrice,marketPrice,duration) values ( %s );'
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
        #print rr[0:6]
        #unicode(rr[3],'shift-jis').encode('utf-8')
        # change datetime format for mySql
        ymd = rr[1].split('/')
        ymd_date = datetime.date(int(ymd[0]),int(ymd[1]),int(ymd[2]))
        print ymd_date.strftime("%Y-%m-%d")
        
    
        return params

    def dataSelect1(self,ndays):
        print "dataSelect1"
        dateObj = MyDateClass()
        dg = u'ŠO—p'
        t = dateObj.timeDeltaDays(ndays)
        sqlstat = 'select clientName,drugName,amount,issueDate,days,drugClarify,officialPrice from expectation \
                   where issuedate >= \'%s\' and drugClarify = \'%s\' order by drugName, issueDate'
        print sqlstat % (t,dg)
        return sqlstat % (t,dg)
    
    def summary(self,dbObj):
        """
        row data 
        """
        ndays = 120
        sqlstat = self.dataSelect1(ndays)
        rwdata = dbObj.selectRecord(sqlstat)
        drMap = {}
        drMapRecent = {}
        
        dateObj = MyDateClass()
        for rt in rwdata: 
            if rt[1] not in drMap:
                datalists = {}
                datalists["count"] = 1
                datalists["amount"] = rt[2]
                drMap[rt[1]] = datalists
            else:
                wklists = {}
                wklists = drMap[rt[1]] 
                wklists["count"] += 1
                wklists["amount"] += rt[2]
                drMap[rt[1]] = wklists
        
        for rt in [ r for r in rwdata if dateObj.timeDeltaDays(30) < r[3]]:
            if rt[1] not in drMapRecent:
                datalists = {}
                datalists["count"] = 1
                datalists["amount"] = rt[2]
                drMapRecent[rt[1]] = datalists
            else:
                wklists = {}
                wklists = drMapRecent[rt[1]] 
                wklists["count"] += 1
                wklists["amount"] += rt[2]
                drMapRecent[rt[1]] = wklists

        for rkey in drMapRecent:
            gammaObj = pyGammaClass()
            pC = drMap[rkey]["count"]
            fC = drMapRecent[rkey]["count"]
            pAmt = drMap[rkey]["amount"]
            fAmt = drMapRecent[rkey]["amount"]
            pAvg = pAmt / pC 
            aAvg = fAmt / fC
            
            alpha = float(pAmt+fAmt)
            lamda = float(pC+fC)
            #print rkey,alpha,lamda
            if pAmt <= 500:
                gammaObj.setParameter(alpha,1/lamda)
                print rkey,gammaObj.getPPF(0.99),alpha/lamda,alpha/(lamda ** 2)
                #print pC,fC,pAmt,fAmt,alpha,lamda

            
        
        #for ritem in rwdata:
        #    drMap[ritem[1]] += ritem[2]
        #drMap[r[1]] += (r[2] for r in rwdata if r[1] in drMap) 
        #print drMap
        
def main():

    expectObj = expectationClass()
    CacheDBObj = CacheDB('receipty')
    try:
        with CacheDBObj:
            #delete exisiting all records
            sqlstat = expectObj.summary(CacheDBObj)
            
            """
            for ritem in r:
                print ritem[1],ritem[3],ritem[2]
            pass
            """
    except:
        print " *** Unexpected error (receiptyDataLoader - main) *** :", sys.exc_info()[0]
    
if __name__ == '__main__':
    main()

    
    