#coding: utf-8

import sys
import datetime
import re
import readCSVF

class drugMasterClass(object):
    
    attributes = ['drugCoe','drugName']
    
    def __init__(self):
        self.drugCode = None
        self.drugName = None
        
    def inserter(self,param):
       sqlbase = 'insert into DrugMaster  (drugCode, drugName) values ( %s );'
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
        sqlstat = 'select drugCode,drugName from DrugMaster order by drugName'
        #print sqlstat 
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
        rsplit = regex2.split(rr[4].decode('cp932'))
        #print rsplit
        #rsplit = rr[2].split('\s')
        params.append(rr[2])
        
        objChar = u'リンデロン'
        rightChar = u'リンデロン－'
        rightChar2 = u'白色ワセリン'
        rightChar3 = u'ハーフジゴ'
        rightChar4 = u'アスパラ－ＣＡ'

        targetChar0 = u'ハ-フジゴキシンＫＹ錠0.125mg'
        sourceChar0 = u'ハーフジゴキシンＫＹ錠０．１２５'
        
        if rightChar in rsplit[0]:
            print "Before : ", rsplit[0]
            regex3 = re.compile(ur"(\S+)－(\S+)" ,re.UNICODE)
            newrep = regex3.sub(ur"\1‐\2",rsplit[0])
            print "After : ", newrep
            params.append(newrep)
        elif rightChar2 in rsplit[0]:
            print "Before : ", rsplit[0]
            regex3 = re.compile(ur"(\S+)（(\S+)" ,re.UNICODE)
            newrep = regex3.sub(ur"\1＊（\2",rsplit[0])
            print "After : ", newrep
            params.append(newrep)
        elif rightChar3 in rsplit[0]:
            print "Before : ", rsplit[0]
            regex3 = re.compile(ur"(\w)ー(\S+)錠０．１２５" ,re.UNICODE)
            newrep = regex3.sub(ur"\1-\2錠0.125mg",rsplit[0])
            print "After : ", newrep
            params.append(newrep)
        elif rightChar4 in rsplit[0]:
            print "Before : ", rsplit[0]
            regex4 = re.compile(ur"(\S+)－(\S+)" ,re.UNICODE)
            newrep = regex4.sub(ur"\1‐\2",rsplit[0])
            print "After : ", newrep
            params.append(newrep)


        else:
            params.append(rsplit[0])
        
        return params
       