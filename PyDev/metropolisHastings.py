#coding: utf-8
from __future__ import division


import math
import sys
#import logging
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from random import random
from random import seed
from ClassException import ClassException
from ClassLogging import ClassLogging


class metropolisHastings(object):
    
    def __init__(self,dbsw=False,pltsw=False):
        self.params = [] 
        
        self.m1 = 0.0
        self.n1 = 0.0
        self.n1S1 = 0.0
        self.mu1 = 0.0
        
        self.mu = 0.0
        self.sigma = 0.0
        
        self.mu_array = np.array([])
        self.std_array = np.array([])
        
        self.debug = dbsw
        self.pltsw = pltsw
        
        if self.debug:
            self.logObj = ClassLogging("_metropolis_")
        else:
            pass
            #print "** Non debug **"
            
        seed(1)
        
    def __enter__(self):
        pass
    
    def __exit__(self):
        pass
    
    def log(self,msg):
        if self.debug:
            self.logObj.logging(msg)
    
    def unknownDistributionDataSet(self,params):
        self.params = params
        self.m1 = self.params[0]
        self.n1 = self.params[1]
        self.n1S1 = self.params[2]
        self.mu1 = self.params[3]
    
    def calcPosteriorDistributionProb(self,mu,sigma):
        
        #self.mu = mu
        #self.sigma = sigma
        postdistprob = sigma ** (-1 * self.n1 - 3) * \
                math.exp(-1 * (self.n1S1 + self.m1 * np.power((mu - self.mu1),2)) / 2 / sigma ** 2  ) 
    
        self.log(" (calcPosteriorDistributionProb)" )
        self.log(" -->  m1 : %2.8f n1 : %2.8f n1S1 : %2.8f mu1 : %2.8f" % (self.m1,self.n1,self.n1S1,self.mu1))
        self.log(" -->  mu : %2.8f sigma : %2.8f" % (mu, sigma))
        self.log("  probability : %2.25f" % postdistprob)
        return postdistprob
    
    def ethaNextStep(self,std):
        
        #mydist = norm(0,std)
        #r = random()
        #etha = mydist.ppf(r)
        etha = np.random.normal(0,std)
        #self.log(" (NextStep)")
        self.log(" etha : %1.4f" % etha )
        return etha
        
    def updateMuAndStd(self):
        
        mm  = self.mu + self.ethaNextStep(0.25)
        ss = self.sigma + self.ethaNextStep(0.25)
        
        self.log("*** (updateMuAndStd :next step process) mm: %2.6f  ss: %2.6f" % (mm,ss))
        
        return (mm,ss)
        
    def startSimulation(self,mu,sigma,nstep):
        
        """
        initial settings
        """
        self.appendMuStd(mu,sigma)
        """
        calculate posterior distribution based on Normal Distribution
        """
        self.mu = mu
        self.sigma = sigma
        for x in np.arange(nstep):
            self.log("------------- [Step : %d of %d (startSimulation)] -----------" % (x,nstep))
            self.probConditions()
        
        if self.pltsw:
            for x in np.arange(nstep):
                self.log("mu:%1.8f sd:%1.8f" % (self.mu_array[x],self.std_array[x]))
                
            self.log("---avg.--- (burn in 1000)")
            self.log("mu:%1.8f sd:%1.8f" % (self.mu_array[1000:].mean(),self.std_array[1000:].mean()) )
            
            fig = plt.figure()
            plt.subplot(211)
            plt.hist(self.mu_array[1000:],bins=40,range=(self.mu_array[1000:].min(),self.mu_array[1000:].max()))
            plt.subplot(212)
            plt.hist(self.std_array[1000:],bins=40,range=(self.std_array[1000:].min(),self.std_array[1000:].max()))
            plt.show()

        
        return ( self.mu_array[1000:].mean(), self.std_array[1000:].mean() )
        
    def appendMuStd(self,mu,sd):
        self.mu_array = np.append(self.mu_array,mu)
        self.std_array = np.append(self.std_array,sd)
    
    def probConditions(self):

        pr0 = self.calcPosteriorDistributionProb(self.mu, self.sigma)
        (mm, ss) = self.updateMuAndStd() # update next position
        pr1 = self.calcPosteriorDistributionProb(mm, ss)
        
        ratio = 0.0    
        if pr0 == 0:
           try:
               raise ClassException()
           except ClassException, E:
               E.ZeroDivide()
               sys.exit(0)            

        else:
            ratio = pr1 / pr0
            
        self.log("  Ratio : %2.10f" % ratio)
        
        if ratio >= 1:
            self.appendMuStd(mm,ss)
            self.mu = mm
            self.sigma = ss
            self.log("  ** Updated ** new data set: %2.10f %2.10f" % (mm,ss))

        else:
            q = random()
            self.log("  Random Number : %2.10f" % q)

            if  ratio >= q:
                self.appendMuStd(mm,ss)
                self.mu = mm
                self.sigma = ss
                self.log("  ** Updated ** new data set: %2.10f %2.10f" % (mm,ss))

            else:
                self.appendMuStd(self.mu,self.sigma)

    def metrop(self,f,mu,sd,nstep,delta=0.25,burn_in = 1000,seeds = 1):
        
        met_iter = self._met(f,mu,sd,nstep,delta,seeds)
        for i, val in enumerate(met_iter):
            if i > burn_in:
                yield val
                break

        for val in met_iter:
            yield val
    
    def _met(self,f,mu,sd,nstep,delta,seeds):
        
        seed(seeds)
        init_x1 = mu
        init_x2 = sd
        init_fx = f(init_x1,init_x2)
    
        for j in range(1,nstep):
            p_x1 = init_x1 + np.random.normal(0,0.20)
            p_x2 = init_x2 + np.random.normal(0,0.20)
            p_fx = f(p_x1,p_x2)
            
            #print p_x1,p_x2,init_fx,p_fx
            
            ratio = p_fx / init_fx
            if ratio > 1. or ratio > random():
                init_x1,init_x2,init_fx = p_x1,p_x2,p_fx
                yield p_x1,p_x2,p_fx
            else:
                yield init_x1,init_x2,init_fx
    
    def mainroutine(self,mu,sigma,nstep):
        
        #print np.power((mu - self.mu1),2)

        postdistprobfunc = lambda mu,sigma: sigma ** (-1 * self.n1 - 3) * \
                math.exp(-1 * (self.n1S1 + self.m1 * np.power((mu - self.mu1),2)) / 2 / sigma ** 2  ) 
        xb1 = []
        xb2 = []
        fxb = []
        for x1,x2,fx in self.metrop(postdistprobfunc,mu,sigma,nstep):
            xb1.append(x1)
            xb2.append(x2)
            fxb.append(fx)
            
        return (np.array(xb1).mean(),np.array(xb2).mean())
        

    
        