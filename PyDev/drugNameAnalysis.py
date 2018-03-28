#coding: utf-8

import datetime
import time
import MySQLdb
import csv
import glob
import math
import numpy as np

# for Japanese Language splitter
import MeCab 
""" 
    for Japanese special setting
"""
import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')
#####

#from readCSFV import testFunc
from CacheDBClass import CacheDB
from expectationClass import expectationClass
import readCSVF

start = time.time()

def progress():
    return True


def elapsed():
    return time.time() - start

def dataRetrieveAndCalc(expectObj,dbObj):
    
    sqlstat = expectObj.drugNameSelect()
    drugdata = dbObj.selectRecord(sqlstat)

    mc = MeCab.Tagger('-Ochasen')

    for w in drugdata[:10]:
        #print w[0]

        encode_text = w[0].encode('utf-8')
        node = mc.parseToNode(encode_text)
        wk_node = node
        #node = node.next
        while wk_node:
            #decode_text = node.surface.decode('utf-8')
            node_before = wk_node.surface 
            print type(node_before),node_before.decode('utf-8')
            wk_node = wk_node.next
            
            
    
def main():
    
    expectObj = expectationClass()
    
    CacheDBObj = CacheDB('receipty')
    try:
        with CacheDBObj:
            ret_code = dataRetrieveAndCalc(expectObj,CacheDBObj)
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

        
if __name__ == '__main__':
    main()
    
    
