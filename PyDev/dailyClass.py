#coding: utf-8

import sys
import datetime
import readCSVF

class dailyClass(object):
    
    attributes = ['cdate','a_no','custNo','fullName','healthIns','institution']
    
    def __init__(self):
        self.id = None
        self.cdate = None
        self.name = None
        self.healthIns = None
        self.custno = None
        self.inst = None    

    def inserter(self,param):
       sqlbase = 'insert into daily (cdate,a_no,custNo,fullName,healthIns,institution) values ( %s );'
       setpieces = []
       values = { 'field1' : 'TESTVAL5', }
       
       data_array = {}
       idx = 0 
       for atr in self.attributes:
           data_array[atr] = param[idx]
           idx = idx + 1
       #print type(param[0]),type(param[1]),type(param[2]),type(param[3]),type(param[4]),type(param[5])
       
       for atr  in self.attributes:
           setpieces.append("%(" + atr + ")s" )
       
       return sqlbase % ',' .join(setpieces), data_array

    def TESTinserter(self,param):
       sqlbase = 'insert into test.daily (cdate,a_no,custNo,fullName,healthIns,institution) values ( %s );'
       setpieces = []
       values = { 'field1' : 'TESTVAL5', }
       
       data_array = {}
       idx = 0 
       for atr in self.attributes:
           data_array[atr] = param[idx]
           idx = idx + 1
       #print type(param[0]),type(param[1]),type(param[2]),type(param[3]),type(param[4]),type(param[5])
       
       for atr  in self.attributes:
           setpieces.append("%(" + atr + ")s" )
       
       return sqlbase % ',' .join(setpieces), data_array

   
    def readFile(self,f,skip=True):
        fhd = readCSVF.readFileCSVEXCEL(f,skip)
        return fhd

    def fieldFormatter(self,rr):
        #print rr[0:6]
        #unicode(rr[3],'shift-jis').encode('utf-8')
        # change datetime format for mySql
        ymd = rr[0].split('/')
        ymd_date = datetime.date(int(ymd[0]),int(ymd[1]),int(ymd[2]))
        #print ymd_date.strftime("'%Y-%m-%d'")
                    
        params = []
        params.append(ymd_date.strftime("%Y-%m-%d"))
        for idx in range(1,6):
            params.append(rr[idx])

            # for the purpose of debugging code                 
            #print len(rr[3]),rr[3],len(unicode(rr[3],'shift-jis'))
            #print len(params[3]),params[3],len(unicode(params[3],'shift-jis'))
            #u1 = u1.decode('utf-8').encode('euc-jp')
            #print u1 
            #ret_code = CacheDBObj.addRecordTest(params[1])
            # EXCEL CSV format --> unicode --> shift jis
        params[1] = int(params[1])
        params[2] = int(params[2])
        # CSV string format cp932 -> unicode 
        params[3] = params[3].decode("cp932")
        params[4] = params[4].decode("cp932")
        params[5] = params[5].decode("cp932")
        #params[3] = unicode(params[3],'shift-jis') 
        #params[4] = unicode(params[4],'shift-jis') 
        #params[5] = unicode(params[5],'shift-jis') 
        
        return params
       