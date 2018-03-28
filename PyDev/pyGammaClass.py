#coding: utf-8

from scipy.stats import gamma

class pyGammaClass(object):
    
    def __init__(self):
        
        self.rv = None
        self.k = None
        self.scale = None
        
    def setParameter(self,k,lamda):       
        try:
            self.rv = gamma(k,0,lamda)
        except:
            print " *** Unexpected error (receiptyDataLoader - main) *** :", sys.exc_info()[0]
        
    def getCDF(self,x):
        return self.rv.cdf(x)
    
    def getPPF(self,pf):
        return self.rv.ppf(pf)

    
    



