#coding: utf-8

import datetime
from dailyClass import dailyClass
from CacheDBClass import CacheDB

def getEncoding(str):
   for encoding in ['utf-8', 'shift-jis', 'euc-jp']:
       try:
           str.decode(encoding)
           return encoding
       except:
           pass
       return None
def main():

    dailyObj = dailyClass()
    #sqlbase = dailyObj.inserter()
    
    CacheDBObj = CacheDB('receipty')
    try:
        with CacheDBObj:
            
            ret_code = CacheDBObj.deleteRecord()
                            
            # Define location of the flat file 
            f = "\\\\EMSCR01\ReceptyN\TEXT\NIKKEI.TXT"
            fhd = dailyObj.readFile(f)
            n = 0
            if fhd is None:
                print "fhd is none."
            else:
                for rr in fhd:
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
                    #print len(rr[3]),rr[3],len(unicode(rr[3],'shift-jis'))
                    #print len(params[3]),params[3],len(unicode(params[3],'shift-jis'))
                    #u1 = u1.decode('utf-8').encode('euc-jp')
                    #print u1 
                    #ret_code = CacheDBObj.addRecordTest(params[1])
                    # EXCEL CSV format --> unicode --> shift jis
                    params[1] = int(params[1])
                    params[2] = int(params[2])
                    params[3] = unicode(params[3],'shift-jis') 
                    params[4] = unicode(params[4],'shift-jis') 
                    params[5] = unicode(params[5],'shift-jis') 

                    data_array = []                    
                    sqlInsertStat, data_array = dailyObj.inserter(params)
                    ret_code = CacheDBObj.addRecordSentence(sqlInsertStat, data_array)
    
                    n = n + 1
            
            print n
            
    except:
        print "Error " 
        return False

if __name__ == '__main__':
    main()