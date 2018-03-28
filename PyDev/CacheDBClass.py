#coding: utf-8

import sys,traceback
import MySQLdb
import readCSVF
#from mysql.connector.errors import Error

class CacheDB(object):
    
    def __init__(self,dbname,remote=False):
        self.con = None;
        self.cur = None;
        self.dbname = dbname;
        self.Error = None;
        
        self.remote = remote
        print "initialize CacheDB."
        
    def __enter__(self):
        
        if not self.remote:
        
            self.usr = "root"
            self.passwd = "robami77"
            #dbname = "test"
        
            print "---- Connect MySQLdb: %s ----" % self.dbname
            self.con = MySQLdb.connect(user=self.usr,passwd = self.passwd, db=self.dbname, charset="utf8")
            self.cur = self.con.cursor()
            #self.Error = MySQLdb.Error
        else:
            self.usr = "emscr03"
            self.passwd = "password"
        
            print "-- Connect MySQLdb: %s  User: %s  Remote DB: %s ----" % (self.dbname,self.usr,self.remote)
            self.con = MySQLdb.connect(host=self.remote, user=self.usr,passwd = self.passwd, db=self.dbname, charset="utf8")
            self.cur = self.con.cursor()
            #self.Error = MySQLdb.Error
            
        
    def __exit__(self,exec_type,exec_values,traceback):
        if exec_type:
            self.con.rollback()
        else:
            print "db Commitment ..."
            self.con.commit()
            self.con.close()
        
        return True

    def changeDatabase(self,dbname):
        print 'changing db ... %s' % (dbname)
        try:
            self.cur.execute("""use %s""", dbname)
            self.con.commit()        
            return True
        except:
            return False

    def deleteRecord(self):
        print "Delete record ... "
        try:
            self.cur.execute("""call deletedaily()""")
            self.con.commit()        
        
            print "DELETE daily record."
        except:
            self.con.rollback()
        return True
    
    def recordProcessWithSql(self,sqlstat):
        
        print "Record Processing Sql statement ... : %s ..." % sqlstat
        try:
            print sqlstat
            self.cur.execute(sqlstat)
            self.con.commit()
        except self.Error, e:
            print "Error  %s " % str(e)
        except:
            print  "Errorin Run function with query"
        
    def selectTestRecord(self):
        print "Select record ... "
        try:
            self.cur.execute(""" select * from stockmaster limit 2""")
            print "select daily record."
            
            records = self.cur.fetchall()
            #for r in records:
            #    print r[2],type(r[2])
            return records    
            #self.con.commit()
    
        except:
            self.con.rollback()
        return True
    
    def selectRecord(self,sqlstat):
        #print "Select record ... "
        try:
            print sqlstat
            self.cur.execute(sqlstat)
            print "select record."
            
            records = self.cur.fetchall()
            #for r in records:
            #    print r[2],type(r[2])
            return records    
            #self.con.commit()
    
        except:
            self.con.rollback()
        return True

        
    def addRecord(self,item):
        print "Testing ..." 
        return True
                                              
    def addRecordTest(self,param):
        try:
            print "data item inserting ..."
            ins_sent = ("insert into test.test1 (cdate) values(%(cdate)s)")
            data_array = {}
            data_array['cdate'] = param
            
            x = ins_sent % data_array
            print x
            self.cur.execute(ins_sent,data_array)
        #   
        except self.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            return False
        except:
            print "Error SQL"

        return True
        
    def addRecordSentence(self,ins_sent,data_array):
        try:
            #ins_sent = ("insert into test1 (cdate) values(%(cdate)s)")
            #data_array = { 'cdate' : param,}
            x = ins_sent % data_array
            
            #print x
            self.cur.execute(ins_sent,data_array)
            self.con.commit()
        except self.Error, e:
            print "** (CacheDBClass) Error  %s " % str(e)
        except:
            # エラーの情報をsysモジュールから取得
            info = sys.exc_info()
            # tracebackモジュールのformat_tbメソッドで特定の書式に変換
            tbinfo = traceback.format_tb( info[2] )
            # 収集した情報を読みやすいように整形して出力する----------------------------
            print 'Python Error.'.ljust( 80, '=' )
            for tbi in tbinfo:
                print tbi
            print '  %s' % str( info[1] )
            print '\n'.rjust( 80, '=' )

            
            #print  "** (CacheDBClass) Errorin Run function with query"
                
    def addRecordFromFile(self,f):
        try:
            print "data item inserting ..."
            fhd = readCSVF.readFileCSV(f)
            for item in fhd:
                print item[0]
                self.cur.execute('insert into daily (cdate, a_no, custNo, fullName, healthIns, institution) values(%s,%s,?,?,?,?);',
                    (item[0],item[1],item[2],item[3].decode('utf-8'),item[4].decode('utf-8'),item[5].decode('utf-8')))
            self.con.commit()       
        except self.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            return False
        return True    
    
                        
def main():
    db = CacheDB('test')
        
    f = "\\\\EMSCR01\ReceptyN\TEXT\NIKKEI.TXT"
    #rt = readCSVF.readFileCSV(f)
    with db:
        db.deleteRecord()
        db.addRecordFromFile(f)
       #db.addRecordTest()
        

if __name__ == '__main__':
    main()
    
    
    