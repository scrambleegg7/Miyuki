#coding: utf-8

import datetime
import time
import MySQLdb
import csv
import glob
import sys
import math
import numpy as np
#from readCSFV import testFunc
from CacheDBClass import CacheDB
from dailyClass import dailyClass
from expectationClass import expectationClass
from stockMasterClass import stockMasterClass
from pyGammaClass import pyGammaClass
from probBasedSDClass import probBasedSDClass

import readCSVF

start = time.time()

def progress():
    return True


def elapsed():
    return time.time() - start


def gammaProb():
    
    pass

def grabStockMaster(dbObj):

    stockObj = {}
    stockMasterObj = stockMasterClass()

    sqlstat = stockMasterObj.dataSelect1()
    rwdata = dbObj.selectRecord(sqlstat)
    
    for rr in rwdata:
        dl = []
        dl.append(rr[1]) # drugName
        dl.append(rr[4]) # current Amount
        stockObj[rr[0]] = dl
    
    return stockObj

def gammaDist(alpha,lamda):
    #print alpha,lamda
    gammaObj = pyGammaClass()
    gammaObj.setParameter(alpha,1/lamda)
    return gammaObj.getPPF(0.99)    

def knownDistributions(params):
    """
    params = [counts, mu., sd, mu0, sd0]
    
    mu = sample mean
    sd = sample standard deviation
    mu0 = population mean
    sd0 = population standard deviation
    
    """
    probBasedSDObj = probBasedSDClass(params)
    probBasedSDObj.setDataKnownSigma()    
    #print (probBasedSDObj.calcMu1(),probBasedSDObj.calcSimga1())
    return (probBasedSDObj.calcMu1(),probBasedSDObj.calcSimga1())

def safeStockCalc(params,ndays):
    
    mu1 = params[0] # mean based on Bayes expectations
    sd1 = params[1] # standard deviation based on Bayes expectations
    
    maxStock = sd1 * math.sqrt(ndays) + mu1 
    return maxStock

def dataRetrieveAndCalc(expectObj,dbObj):
    
    ndays120 = 180
    ndays30 = 30
        
    sqlstat = expectObj.dataSelect1(ndays120)
    rwdata120 = dbObj.selectRecord(sqlstat)

    sqlstat = expectObj.dataSelect1(ndays30)
    rwdata30 = dbObj.selectRecord(sqlstat)
    
    drMap = {}
    drMapRecent = {}
        
    for rt in rwdata120: 
        if rt[0] not in drMap:
            n_array = np.array([])
            n_array = np.append(n_array,rt[3])
            drMap[rt[0]] = n_array 
        else:
            n_array = drMap[rt[0]] 
            n_array = np.append(n_array,rt[3])
            drMap[rt[0]] = n_array
    
    pastStockList = {}
    for rt in rwdata30:
        #print rt[2]
        if rt[0] not in pastStockList:
            pastStockList[rt[0]] = rt[2]
        
        if rt[0] not in drMapRecent:
            n_array = np.array([])
            n_array = np.append(n_array,rt[3])
            drMapRecent[rt[0]] = n_array
        else:
            n_array = drMapRecent[rt[0]] 
            n_array = np.append(n_array,rt[3])
            drMapRecent[rt[0]] = n_array
         
    stockObj = grabStockMaster(dbObj)
    
    #print drMapRecent
    for rkey in drMapRecent:
        #print rkey    
        prvArray = drMap[rkey]
        forArray = drMapRecent[rkey]
        alpha = prvArray.sum() + forArray.sum()
        lamda = prvArray.size + forArray.size

        
        if rkey not in stockObj:
            print " ------ ZERO Stock : %s %s" % (rkey,pastStockList[rkey]) 
            continue
        else:
            dl = stockObj[rkey]
        #print dl[0],prvArray.sum(),dl[1]
        #print "-- rkey : %s alpha : %4.4f lamda : %4.4f" % (dl[0],alpha,lamda)
        if prvArray.sum() <= 300:
            if lamda <= 0:
                lamda = 1 
            gx = gammaDist(float(alpha),float(lamda))
            #print "-- gx : ",gx    
            if gx > dl[1]:
                print "** ** %s %s Stock:%4.4f  Expect:%4.4f (Gamma Distribution)" % (rkey,dl[0],dl[1],gx)
            #else: 
                #print "nothing"
        else:    
            params = []
            sd = forArray.std()
            params.append(forArray.size)
            params.append(forArray.mean())
            if forArray.std() <= 0.0:
                params.append(1.0)
            else:    
                params.append(forArray.std())
            params.append(prvArray.mean())
            if prvArray.std() <= 0.0:
                params.append(1.0)
            else:
                params.append(prvArray.std())
            
            
            
            results = knownDistributions(params)
            maxS =  safeStockCalc(results,14)
            if maxS > dl[1]:
                print "** ** %s %s Stock:%4.4f  Expect:%4.4f (Standard Deviation)" % (rkey,dl[0],dl[1],maxS)

    return True

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
    
    
