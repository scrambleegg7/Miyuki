#coding: utf-8

import sys
import datetime
import re
import numpy as np

import readCSVF

from MyDateClass import MyDateClass
from CacheDBClass import CacheDB
#from pyGammaClass import pyGammaClass

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

    def drugNameSelect(self):
        #print "dataSelect1"
        sqlstat = 'select drugName from expectation' 
        #           where issuedate >= \'%s\' and drugClarify = \'%s\' order by drugName, issueDate'
        print sqlstat 
        return sqlstat 

    def dataSelect1(self,ndays):
        #print "dataSelect1"
        dateObj = MyDateClass()
        dg = u'外用'
        t = dateObj.timeDeltaDays(ndays)
        sqlstat = 'select drugCode,clientName,drugName,amount,issueDate,days,drugClarify,officialPrice from expectation \
                   where issuedate >= \'%s\' and drugClarify = \'%s\' order by drugName, issueDate'
        print sqlstat % (t,dg)
        return sqlstat % (t,dg)

    def dataSelect2(self,ndays):
        #print "dataSelect1"
        dateObj = MyDateClass()
        dg = u'内服'
        na = u'%宮崎%'
        t = dateObj.timeDeltaDays(ndays)
        sqlstat = 'select drugCode,clientName,drugName,amount,issueDate,days,drugClarify,officialPrice from expectation \
                   where issuedate >= \'%s\' and drugClarify = \'%s\' order by drugName, issueDate'
        print sqlstat % (t,dg)
        return sqlstat % (t,dg)

    def dataSelect3(self,ndays):
        #print "dataSelect1"
        dateObj = MyDateClass()
        dg = u'内服'
        t = dateObj.timeDeltaDays(ndays)
        sqlstat = 'select drugCode,issueDate,datediff(issuedate,\'%s\') as days, sum(amount * days) as total from expectation \
                   where issuedate >= \'%s\' and drugClarify = \'%s\' group by drugCode, issuedate order by drugcode, issueDate'
        print sqlstat % (t,t,dg)
        return sqlstat % (t,t,dg)

    
    def summary(self,dbObj):
        pass
        """
        row data 
        
        ndays120 = 120
        ndays120 = 30
        
        sqlstat = self.dataSelect1(ndays120)
        rwdata120 = dbObj.selectRecord(sqlstat)
        sqlstat = self.dataSelect1(ndays30)
        rwdata30 = dbObj.selectRecord(sqlstat)
        
        drMap = {}
        drMapRecent = {}
        rObj = {}
        
        dateObj = MyDateClass()
        for rt in rwdata120: 
            if rt[0] not in drMap:
                n_array = np.array([])
                n_array = np.append(n_array,rt[3])
                drMap[rt[0]] = n_array
            else:
                n_array = drMap[rt[1]] 
                n_array = np.append(n_array,rt[3])
                drMap[rt[0]] = n_array
        
        for rt  in rwdata30:
            if rt[0] not in drMapRecent:
                n_array = np.array([])
                n_array = np.append(n_array,rt[3])
                drMapRecent[rt[0]] = datalists
            else:
                n_array = drMapRecent[rt[1]] 
                n_array = np.append(n_array,rt[3])
                drMapRecent[rt[0]] = wklists

        for rkey in drMapRecent:
#           
            pA = drMap[rkey]
            fA = drMapRecent[rkey]
            pC = pA.size
            fC = fA.size
            pAmt = 
            fAmt = drMapRecent[rkey]["amount"]
            pAvg = pA.sum / pC 
            aAvg = fAmt / fC
            arr_amt = drMapRecent[rkey]["arr_amt"]
            
            #alpha = float(pAmt+fAmt)
            #lamda = float(pC+fC)
            #print rkey,alpha,lamda
            if pAmt <= 500:
                uObj = []
                uObj = ()
                uObj = (float(pAmt),float(alpha),float(lamda))
                rObj[rkey] = uObj
            else:
                uObj = []
                uObj = ()
                uObj = (float(pAmt),float(alpha),float(lamda),arr_amt)
                rObj[rkey] = uObj
            
                #gammaObj.setParameter(alpha,1/lamda)
                #print rkey,gammaObj.getPPF(0.99),alpha/lamda,alpha/(lamda ** 2)
                #print pC,fC,pAmt,fAmt,alpha,lamda
        
        return rObj
        """    
        
'''        
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

    
'''    