#coding: utf-8

import csv
import codecs

def main(fileName):
    if fileName:
        rf = readFile(fileName)
        ret_flag = outPut(rf)
    else:
        print "sorry, we need FileName."

def readFileCSV(fileName):
    print "reading : ", fileName, " ..."
    rf = open(fileName,"rb")
    #dialect = csv.excel
    fhandler = csv.reader(rf,dialect)
    return fhandler
    #records = [map(int,x) for x in inc]

def readFileCSVEXCEL(fileName,skip):
    print "reading : ", fileName, " ..."
    rf = open(fileName,"rb")
    dialect = csv.excel
    fhandler = csv.reader(rf,dialect)
    
    if skip:
        fhandler.next()
    
    return fhandler
    #records = [map(int,x) for x in inc]
    
def readFile(fileName):
    print "reading normal flat file : ", fileName, " ..."
    rf = open(fileName,"rb")
    return rf
    
def readFileCodex(fileName,cd):
    print "reading : ", fileName, " ..."
    rf = codecs.open(fileName,"rb",cd)
    inc = csv.reader(rf)
    
    return inc

def outPut(r):
    #for row in r:
    #    print row[0],row[1],row[2],row[3],row[4],row[5]
    return True

def testFunc(param1):
    print 'test parameter ',  param1
    return True
                
if __name__ == '__main__':
    f = "\\\\EMSCR01\ReceptyN\TEXT\NIKKEI.TXT"
    testFunc(f)