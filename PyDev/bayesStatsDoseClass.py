#coding: utf-8
from __future__ import division
import datetime
import time
import MySQLdb
import csv
import glob
import sys, traceback
import math
import copy 
import numpy as np
import matplotlib.pyplot as plt
#from readCSFV import testFunc
from CacheDBClass import CacheDB
from dailyClass import dailyClass
from expectationClass import expectationClass
from stockMasterClass import stockMasterClass
from weeklyDrugClass import weeklyDrugClass
from drugMasterClass import drugMasterClass
from pyGammaClass import pyGammaClass
from probBasedSDClass import probBasedSDClass
from ClassLogging import ClassLogging
from datetime import timedelta
from MyDateClass import MyDateClass
from probBasedSDClass import probBasedSDClass
from metropolisHastings import metropolisHastings

from bayesRegression import bayesRegression
from forwardClientClass import forwardClientClass

import readCSVF

forwardCalcfunc1 = lambda d,nd : d + timedelta(days=nd)
    

class bayesStatsDoseClass(object):
    
    def __init__(self,dbObj):
   
        self.start = time.time()
#        self.logObj = ClassLogging("bayesStatsDose")
        self.debug = True
        
        self.drugMasterObj = {}
        self.stockMasterObj = {}
        self.weeklyMap = {}

        self.mydateObj = MyDateClass()
    
        self.dbObj = dbObj
        self.stockMasterObj = self.grabStockMaster(dbObj)
        self.drugMasterObj = self.grabDrugMaster(dbObj)
        self.weeklyMap = self.grabWeekyDrugMap(dbObj)
        
        self.forwardClient = []
        
        if self.debug:
            self.logObj = ClassLogging("_bayesStatsDose_")
    
    def __enter__(self):
        self.deleteforwardClient(self.dbObj)
        self.startProcess(self.dbObj)
        self.insertforwardClient(self.dbObj)
        
    def __exit__(self,exec_type,exec_values,traceback):
        pass
        
    def elapsed(self):
        return time.time() - self.start
    
    def log(self,msg):
        if self.debug:
            self.logObj.logging(msg)

    def gammaDist(self,alpha,lamda):
        #print alpha,lamda
        gammaObj = pyGammaClass()
        gammaObj.setParameter(alpha,1/lamda)
        return gammaObj.getPPF(0.99)    
    
    def grabDrugMaster(self,dbObj):

        drugObj = drugMasterClass()
        sqlstat = drugObj.dataSelect1()
        rwdata = dbObj.selectRecord(sqlstat)
        drugMObj = {}
        drugMObj = dict(zip([rr[0] for rr in rwdata],[rr[1] for rr in rwdata]))
        
        return drugMObj
    
    def grabStockMaster(self,dbObj):

        stockMObj = stockMasterClass()
        sqlstat = stockMObj.dataSelect1()
        rwdata = dbObj.selectRecord(sqlstat)
    
        stockObj = {}
        for rr in rwdata:
            dl = []
            dl.append(rr[1]) # drugName
            dl.append(rr[4]) # current Amount
            stockObj[rr[0]] = dl
    
        return stockObj
    
    def grabWeekyDrugMap(self,dbObj):

        weeklyDrugObj = weeklyDrugClass()
        sqlstat = weeklyDrugObj.dataSelect1()
        rwweekly = dbObj.selectRecord(sqlstat)
        weeklyM = {}
        weeklyM = dict(zip( [x[0] for x in rwweekly], [x[2] for x in rwweekly]) )
        return weeklyM

    def deleteforwardClient(self,dbObj):
        
        sqlstat = "delete from forwardClient"
        ret_code = dbObj.recordProcessWithSql(sqlstat)

    def insertforwardClient(self,dbObj):
        
        forwardClientObj = forwardClientClass()
        for data in self.forwardClient:
            params = forwardClientObj.fieldFormatter(data)
            data_array = []                    
            sqlInsertStat, data_array = forwardClientObj.inserter(params)
            #print sqlInsertStat, data_array
            ret_code = dbObj.addRecordSentence(sqlInsertStat, data_array)
            

    def startProcess(self,dbObj):
        
        #ret_code = self.grabTradeData(dbObj)
        ret_code = self.grabTradeDataIter(dbObj)
        
    def grabTradeData(self,dbObj):
        ndays180 = 180
        
        print "grab trade...."
        expectObj = expectationClass()
        sqlstat = expectObj.dataSelect2(ndays180)
        rwdata180 = dbObj.selectRecord(sqlstat)

        ls = set([rr[0] for rr in rwdata180]) #unique drugCode
    
        mydict = {}    
        mydict_total = {}
        mydict_forwardtotal = {}
    
        for dcode in ls:
            myarray = np.array([rr[4] for rr in rwdata180 if rr[0] == dcode])
        
            if dcode in self.weeklyMap:
                kn = self.weeklyMap[dcode]
            else:
                kn = 1
            
            ndarray = np.array([forwardCalcfunc1(rr[4], rr[5] * kn) for rr in rwdata180 if rr[0] == dcode])
            forwardfromTodays_list = [(dd - self.mydateObj.getToday()).days for dd in ndarray]
            amtarray = np.array([ (rr[3] * rr[5]) for rr in rwdata180 if rr[0] == dcode])
                
            ulist = []
            rss = [rr for rr in rwdata180 if rr[0] == dcode]
            for idx,rr in enumerate(rss) :
                rl = list(rr)
                rl.append(ndarray[idx])   # rr[8]
                rl.append(forwardfromTodays_list[idx]) # rr[9]
                rl.append(amtarray[idx])   # rr[10]
                tp_rl = tuple(rl)
                ulist.append(rl)
             
            non_visitinglist = self.getVisitDrN(ulist)
            
            v = [rr[10] for rr in non_visitinglist]  # amount 
            v_array = np.array(v)
            mu = v_array.mean()
            std = v_array.std()

            
            if std == 0:
                msg = "*std zero*"
                
                """
                apply gamma distribution process for standard deviation ZERO
                its standard model of using mean/std x n does not cover future data movements. 
                """
                alpha = v_array.sum()
                lamda = v_array.size 

                if lamda <= 0:
                    lamda = 1 
                gx = self.gammaDist(float(alpha),float(lamda))
                params = [dcode,non_visitinglist,gx,(gx * 0.5)]
                ret_code = self.stockMasterCheckWithMean(params,msg)
            else:
                p = [v_array.size,mu,std,mu,std]
                probBasedSDObj = probBasedSDClass(p)
                rt = probBasedSDObj.getDataPriorGammaDistribution()    
    
                mtp = metropolisHastings(False,False)
                mtp.unknownDistributionDataSet(rt)
                #(m,sg) = mtp.startSimulation(mu,mu,5000)
                (m,sg) = mtp.mainroutine(mu,std,10000)
                
                params = [dcode,non_visitinglist,m,sg]    
                ret_code = self.stockMasterCheckWithMean(params," ")

        return True

    def getVisitDrN(self,ulist):
        res = False
        cp_ulist = copy.deepcopy(ulist) #deep copy
        """
        rr[0] drugCode 
        rr[1] clientName
        rr[2] drugName
        rr[3] amount per days
        rr[4] issueDate
        rr[5] days
        rr[6] drugClarify
        rr[7] officialPrice
        rr[8] nextissuedate
        rr[9] days of nextissuedate from Today
        rr[10] total amount per drug per one sale 
        """
        non_visitinglist = []
        for idx,rr in enumerate(ulist):
            """
            +/- 6 days from nextisuedate
            """
            m10d = forwardCalcfunc1(rr[8], -6)
            p10d = forwardCalcfunc1(rr[8], 6)
        
            if rr[9] < 0 and rr[9] >= 30:
                """
                exact match from 30 days prior to today until yesterday
                """
                t_cprr = np.array([ cprr for cprr in cp_ulist if cprr[1] == rr[1] and cprr[4] == rr[8] ] )
                if t_cprr.size > 0: 
                    pass
                    #print "M %s %s %s %s pos:%d" % (rr[1],rr[2],rr[4].strftime('%Y%m%d'),rr[8].strftime('%Y%m%d'),idx)
                else:
                    t_cprr = np.array([ cprr for cprr in cp_ulist if cprr[1] == rr[1] and cprr[4] >= m10d and cprr[4] <= p10d ] )
                    if t_cprr.size > 0:
                        pass
                        #print "  %s %s %s %s pos:%d" % (rr[1],rr[2],rr[4].strftime('%Y%m%d'),rr[8].strftime('%Y%m%d'),idx)
                    else:
                        print "N  %s %s %s %s pos:%d" % (rr[1],rr[2],rr[4].strftime('%Y%m%d'),rr[8].strftime('%Y%m%d'),idx)
                        non_visitinglist.append(rr)
            
            if rr[9] >=0:
                t_cprr = np.array([cprr for cprr in cp_ulist if cprr[9] >=0 and cprr[1] == rr[1] and cprr[4] >= m10d and cprr[4] <= p10d] )
                if t_cprr.size > 0:
                    pass
                else:
                    print "N  %s %s %s %s pos:%d" % (rr[1],rr[2],rr[4].strftime('%Y%m%d'),rr[8].strftime('%Y%m%d'),idx)
                    non_visitinglist.append(rr)
                
        return non_visitinglist

    def grabTradeDataIter(self,dbObj):
        ndays180 = 180
        
        print "grab trade...."
        expectObj = expectationClass()
        sqlstat = expectObj.dataSelect2(ndays180)
        rwdata180 = dbObj.selectRecord(sqlstat)

        ls = set([rr[0] for rr in rwdata180]) #unique drugCode
    
        for dcode in ls:
            rss = [rr for rr in rwdata180 if rr[0] == dcode]
            ulist = self.rwdataIterfunc(rss,dcode)
            non_visitinglist = self.getVisitDrIterFunc(ulist)
            
            if len(non_visitinglist) == 0: continue
            
            v = [rr[10] for rr in non_visitinglist]  # amount 
            v_array = np.array(v)
            mu = v_array.mean()
            std = v_array.std()

            #params = [dcode,non_visitinglist,mu,0.]
            if std == 0:
                msg = "*std zero*"
                """
                apply gamma distribution process for standard deviation ZERO
                its standard model of using mean/std x n does not cover future data movements. 
                """
                alpha = v_array.sum()
                lamda = v_array.size 

                #print dcode,float(alpha),float(lamda)
                if lamda <= 0:
                    lamda = 2.0 
                gx = self.gammaDist(alpha, lamda)
                params = [dcode,non_visitinglist,gx,0.0]
                ret_code = self.stockMasterCheckWithMean(params,msg)
            else:
                p = [v_array.size,mu,std,mu,std]
                probBasedSDObj = probBasedSDClass(p)
                rt = probBasedSDObj.getDataPriorGammaDistribution()    
    
                mtp = metropolisHastings(False,False)
                mtp.unknownDistributionDataSet(rt)
                #(m,sg) = mtp.startSimulation(mu,mu,5000)
                (m,sg) = mtp.mainroutine(mu,std,10000)
                
                params = [dcode,non_visitinglist,m,sg]    
                ret_code = self.stockMasterCheckWithMean(params," ")

        return True

    def rwdataIterfunc(self,rss,dcode):

        if dcode in self.weeklyMap:
            kn = self.weeklyMap[dcode]
        else:
            kn = 1
        
        ulist = []
        iter = self._rwdataIterGen(rss,kn)
        ulist = [val for i,val in enumerate(iter)]
        #    ulist.append(val)
        
        return ulist
        
    def _rwdataIterGen(self,rss,k):
        
        for idx,rr in enumerate(rss) :
            rl = list(rr)

            dd = forwardCalcfunc1(rr[4], rr[5] * k)
            forwardfromTodays = (dd - self.mydateObj.getToday()).days 
            amt = (rr[3] * rr[5]) 
            rl.append(dd)   # rr[8]
            rl.append(forwardfromTodays) # rr[9]
            rl.append(amt)   # rr[10]
            tp_rl = tuple(rl)
            yield rl

    def getVisitDrIterFunc(self,ulist):
        
        non_visitinglist = []
        iter = self._getVisitDrGen(ulist)
        non_visitinglist = [v for idx, v in enumerate(iter)]
            
        return non_visitinglist

    def _getVisitDrGen(self,ulist):
        res = False
        cp_ulist = copy.deepcopy(ulist) #deep copy
        """
        rr[0] drugCode 
        rr[1] clientName
        rr[2] drugName
        rr[3] amount per days
        rr[4] issueDate
        rr[5] days
        rr[6] drugClarify
        rr[7] officialPrice
        rr[8] nextissuedate
        rr[9] days of nextissuedate from Today
        rr[10] total amount per drug per one sale 
        """
        non_visitinglist = []
        for idx,rr in enumerate(ulist):
            """
            +/- 8 days from nextisuedate
            """
            m10d = forwardCalcfunc1(rr[8], -8)
            p10d = forwardCalcfunc1(rr[8], 8)

            if rr[9] < 0 and rr[9] >= -30:
                """
                exact match from 30 days prior to today until yesterday
                """
                t_cprr = np.array([ cprr for cprr in cp_ulist if cprr[1] == rr[1] and cprr[4] == rr[8] ] )
                if t_cprr.size > 0: 
                    pass
                    #print "M %s %s %s %s pos:%d" % (rr[1],rr[2],rr[4].strftime('%Y%m%d'),rr[8].strftime('%Y%m%d'),idx)
                else:
                    t_cprr = np.array([ cprr for cprr in cp_ulist if cprr[1] == rr[1] and cprr[4] >= m10d and cprr[4] <= p10d ] )
                    if t_cprr.size > 0:
                        pass
                        #print "  %s %s %s %s pos:%d" % (rr[1],rr[2],rr[4].strftime('%Y%m%d'),rr[8].strftime('%Y%m%d'),idx)
                    else:
                        print "N  %s %s %s %s pos:%d" % (rr[1],rr[2],rr[4].strftime('%Y%m%d'),rr[8].strftime('%Y%m%d'),idx)
                        yield rr
            
            if rr[9] >=0:
                t_cprr = np.array([cprr for cprr in cp_ulist if cprr[9] >=0 and cprr[1] == rr[1] and cprr[4] >= m10d and cprr[4] <= p10d] )
                if t_cprr.size > 0:
                    pass
                else:
                    print "N  %s %s %s %s pos:%d" % (rr[1],rr[2],rr[4].strftime('%Y%m%d'),rr[8].strftime('%Y%m%d'),idx)
                    yield rr
    
    def checkVisitDr(self,dcode,namearray,ndarray,issuearray,amtarray,drugNamearray):
        res = False
        x = np.array([])
        self.log(" -- %s -- " % drugNamearray[0])
        
        tprv = [t for t in ndarray if t < self.mydateObj.getToday()]
        
        #appendfunc = lambda x : na.append
        for idx,nd in enumerate(ndarray):
            """
            check +- 5days from nextissuedate == issuedate
            """
            m10d = forwardCalcfunc1(nd, -5)
            p10d = forwardCalcfunc1(nd, 5)
            for idy,iss in enumerate(issuearray):
                
                
                if nd == iss and namearray[idx] == namearray[idy] and nd >= self.mydateObj.getToday():
                    x = self.appendIndex(x,idy)
                    self.log("M   %s issue:%s next:%s idNo:%d" % (namearray[idy],iss.strftime('%Y%m%d'),nd.strftime('%Y%m%d'),idy))
                elif m10d <= iss and p10d >= iss and namearray[idx] == namearray[idy] and nd >= self.mydateObj.getToday():
                    x = self.appendIndex(x,idy)
                    self.log("    %s issue:%s next:%s idNo:%d" % (namearray[idy],iss.strftime('%Y%m%d'),nd.strftime('%Y%m%d'),idy))
                elif m10d <= iss and p10d >= iss and namearray[idx] == namearray[idy] and nd < self.mydateObj.getToday():
                    pass
                #else:
                    #self.log("N   %s next:%s idNo:%d" % (namearray[idy],nd.strftime('%Y%m%d'),idy))
                    
        return res
    
    def appendIndex(self,x_array,val):
        
        if val not in x_array:
            return np.append(x_array,val)
        else:
            return x_array
    
    def stockMasterCheckWithMean(self,params,msg):
        res = False

        dcode = params[0]
        non_visiting = params[1]
        mu = params[2]
        sd = params[3]

        if dcode in self.stockMasterObj:
            if self.stockMasterObj[dcode][1] < (mu + 2 * sd):
                for i,rr in enumerate(non_visiting):
                    #print rr[8],rr[1],rr[10],self.drugMasterObj[dcode],self.stockMasterObj[dcode][1],mu,sd,msg
                    data = [rr[8],rr[1],rr[10],self.drugMasterObj[dcode],self.stockMasterObj[dcode][1],mu,sd,msg," "]    
                    self.forwardClient.append(data)
        else:
            if mu > 0:
                if dcode in self.drugMasterObj:
                    for i,rr in enumerate(non_visiting):
                        #print rr[8],rr[1],rr[10],self.drugMasterObj[dcode],0.,mu,sd,msg,"- ZERO Stock -"
                        data = [rr[8],rr[1],rr[10],self.drugMasterObj[dcode],0.,mu,sd,msg,"- ZERO Stock -"]
                        self.forwardClient.append(data)

        return res
    
    def stockMasterCheck(self,params,msg):

        dcode = params[0]
        ndarray = params[1]
        namearray = params[2]
        amtarray = params[3]
        mu = params[4]
        sd = params[5]
        
        if dcode in self.stockMasterObj:
            if self.stockMasterObj[dcode][1] < (mu + sd):
                for i,forwardD in enumerate(ndarray):
                    if forwardD >= self.mydateObj.getToday():
                        print forwardD,namearray[i],amtarray[i],self.drugMasterObj[dcode],self.stockMasterObj[dcode][1],mu,msg
                        
                        data = [forwardD,namearray[i],amtarray[i],self.drugMasterObj[dcode],self.stockMasterObj[dcode][1],mu,sd,msg,""]
                        self.forwardClient.append(data)
                        #print "     --- %s : Mean : %2.10f Stock : %d " % (self.drugMasterObj[dcode],mu,self.stockMasterObj[dcode][1])
        else:
            if mu > 0:
                if dcode in self.drugMasterObj:
                    for i,forwardD in enumerate(ndarray):
                        if forwardD >= self.mydateObj.getToday():
                            print forwardD,namearray[i],amtarray[i],self.drugMasterObj[dcode],0.,mu,msg,"- ZERO Stock -"
                            data = [forwardD,namearray[i],amtarray[i],self.drugMasterObj[dcode],0.,mu,sd,msg,"- ZERO Stock -"]
                            self.forwardClient.append(data)
                            #print "      **** Stock ZERO %s " % (self.drugMasterObj[dcode])
                    
        return True