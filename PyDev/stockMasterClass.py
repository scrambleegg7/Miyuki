#coding: utf-8

import sys
import datetime
import re
import readCSVF

class stockMasterClass(object):
    
    attributes = ['drugName','clarification','prevStockNum','currStockNum','unit','officialPrice','marketPrice','stockdate']
    
    def __init__(self):
        self.drugName = None
        self.clarification = None
        self.prevStockNum = None
        self.currStockNum = None
        self.unit = None
        self.officialPrice = None
        self.marketPrice = None
        self.stockdate = None

    def inserter(self,param):
       sqlbase = 'insert into StockMaster  (drugName,clarification,prevStockNum,currStockNum,unit,officialPrice,marketPrice,stockdate) values ( %s );'
       setpieces = []
       
       data_array = {}
       idx = 0 
       for atr in self.attributes:
           data_array[atr] = param[idx]
           idx = idx + 1
       #print type(param[0]),type(param[1]),type(param[2]),type(param[3]),type(param[4]),type(param[5])
       
       for atr  in self.attributes:
           setpieces.append("%(" + atr + ")s" )
       
       return sqlbase % ',' .join(setpieces), data_array

    def readFile(self,f,skip):
        fhd = readCSVF.readFileCSVEXCEL(f,skip)
        return fhd
    
    def dataSelect1(self):
        #print "dataSelect1"
        sqlstat = 'select drugCode,drugName,clarification,prevStockNum,currStockNum,officialPrice from StockMaster \
                    order by drugName'
        print sqlstat 
        return sqlstat 
    

    def fieldFormatter(self,rr):
        #print rr[0:6]
        #unicode(rr[3],'shift-jis').encode('utf-8')
        # change datetime format for mySql
        #ymd = rr[0].split('/')
        #ymd_date = datetime.date(int(ymd[0]),int(ymd[1]),int(ymd[2]))
        #print ymd_date.strftime("'%Y-%m-%d'")
        
        params = []
        ymd = datetime.date.today()
        #params.append(ymd.strftime("%Y-%m-%d"))
        
        # on unicode version, sentence is split out with space (\s+)
        rrsplit = []
        regex2 = re.compile(ur"\s+",re.UNICODE)
        rsplit = regex2.split(rr[2].decode('cp932'))
        #print rsplit
        #rsplit = rr[2].split('\s')
        params.append(rsplit[0])
        params.append(rr[5].decode('cp932'))
        params.append( float(rr[6]) )
        params.append( float(rr[7]) )
        params.append(rr[8].decode('cp932'))
        params.append(float(rr[9]))
        params.append(float(rr[10]))
        params.append(ymd.strftime("%Y-%m-%d"))

        rightChar = u'リンデロン'
        
        if rightChar in rsplit[0]:
            pass
            #print rsplit[0]
            #print rr

            # for the purpose of debugging code                 
            #print len(rr[3]),rr[3],len(unicode(rr[3],'shift-jis'))
            #print len(params[3]),params[3],len(unicode(params[3],'shift-jis'))
            #u1 = u1.decode('utf-8').encode('euc-jp')
            #print u1 
            #ret_code = CacheDBObj.addRecordTest(params[1])
            # EXCEL CSV format --> unicode --> shift jis
        # CSV string format cp932 -> unicode 
        
        return params
       