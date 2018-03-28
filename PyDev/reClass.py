#coding: utf-8

import sys
import datetime
import re
import readCSVF
from StringClass import StringClass

class reClass(object):
    
    attributes = ['receiptyNo','receiptyClass','chodate','fullName','sex','birthDate','institution','inst_address','doctorName']
    #flags = {'national' : 'k', 'tokyo': 's'}
    flags = ['k','s']
    
    def __init__(self):
        self.ksFlag = None
        self.receiptyNo = None
        self.seqNo = None
        self.receiptyClass = None
        self.chodate = None
        self.fullName = None
        self.sex = None
        self.birthDate = None
        self.institution = None
        self.inst_address = None
        self.doctorName = None
        
        self.clientNo = None
        
    def setData(self,findex,params):
        try:
            
            self.ksFlag = self.flags[findex]            
            
            self.receiptyNo = params[3][1:5]
            self.seqNo = params[1]
            self.receiptyClass = params[2]
            self.chodate = params[3]
            self.fullName = StringClass(params[4])
            self.sex = params[5]
            self.birthDate = params[6]            
            self.institution = StringClass(params[12])
            self.inst_address = StringClass(params[13])
            self.doctorName = StringClass(params[14])
            
            self.clientNo = self.ksFlag + self.receiptyNo + '_' + self.seqNo
            
        except:
            print " *** Unexpected error: (setData) *** : ", sys.exc_info()[0]
            raise
        
        return True

    def getClientNo(self):
        return self.clientNo

    def readFile(self,f,skip=True):
        fhd = readCSVF.readFileCSVEXCEL(f,skip)
        return fhd

        
    def inserter(self,param):
       try:
           sqlbase = "insert into re (receiptyNo,receiptyClass,chodate,fullName,sex,birthDate,institution,inst_address,doctorName) values(%s) "
           setpieces = []
           data_array = {}
        
           for idx, atr in enumerate(self.attributes):
               data_array[atr] = param[idx]
           for atr  in self.attributes:
               setpieces.append("%(" + atr + ")s" )
       
           return sqlbase % ',' .join(setpieces), data_array
       except:
            print " *** Unexpected error (inserter) *** :", sys.exc_info()[0]


    def fieldFormatter(self):
        #print rr[0:6]
        #unicode(rr[3],'shift-jis').encode('utf-8')
        # change datetime format for mySql
        try:
            params = []
            params.append(self.ksFlag + self.receiptyNo + '_' + self.seqNo)
            params.append(int(self.receiptyClass))
            params.append(self.chodate)
            params.append(self.fullName.cp932Converter())
            params.append(self.sex)
            params.append(self.birthDate)
            params.append(self.institution.cp932Converter())
            params.append(self.inst_address.cp932Converter())
            params.append(self.doctorName.cp932Converter())
        
            return params
        except:
            print "Unexpected error(fieldFormatter):", sys.exc_info()[0]
            
        
        
def main():
    in_params = sys.argv
    
    for x in in_params:
        print type(x), x
    
    print 
    

    
if __name__ == '__main__':
     main()   