#coding: utf-8

import math
from metropolisHastings import metropolisHastings

class ClassException(BaseException):
    def muException(self):
        print "No !! Please use setDataKnownSigma method !!"
        
class probBasedSDClass(object):

    def __init__(self,params):
        self.n = 0.
        self.mu = 0.
        self.sigma = 0.
        self.mu0 = 0.
        self.sigma0 = 0.
        
        self.mu1 = 0.
        self.sigma1 = 0.

        self.n = params[0]
        self.mu = params[1]
        self.sigma = params[2]
        self.mu0 = params[3]
        self.sigma0 = params[4]
        self.knownSigma = True 
        
        self.knownSigma = False 

        try:
            val = 1 / self.sigma
        except ZeroDivisionError:
            self.sigma = 1

        try:
            val = 1 / self.sigma0
        except ZeroDivisionError:
            self.sigma0 = 1

        
    def __enter__(self):
        pass
        
    def __exit__(self):
        pass
    
    def setDataKnownSigma(self):
        """
        self.n = params[0]
        self.mu = params[1]
        self.sigma = params[2]
        self.mu0 = params[3]
        self.sigma0 = params[4]
        """
        self.knownSigma = True 
    
        try:
            val = 1 / self.sigma
        except ZeroDivisionError:
            self.sigma = 1

        try:
            val = 1 / self.sigma0
        except ZeroDivisionError:
            self.sigma0 = 1
     
    
    def setDataUnKnownSigma(self,params):
        self.n = params[0]
        self.mu = params[1]
        self.sigma = params[2]
        self.mu0 = params[3]
        self.sigma0 = params[4]
        self.knownSigma = False 
        
    def calcMu1(self):
        
        if self.knownSigma:
            wk0 = (self.n * self.mu / self.sigma ** 2) + (self.mu0 / self.sigma0 ** 2)  
            wk1 = (self.n / self.sigma ** 2) + 1 / self.sigma0 ** 2
            self.mu1 = wk0 / wk1
        
            return self.mu1
        else:
            try:
                raise ClassException()
            except ClassException, E:
                E.muException()

    def calcSimga1(self):

        if self.knownSigma:        
            wk0 = (self.n / self.sigma ** 2) + (1 / self.sigma0 ** 2)
            self.sigma1 = 1 / wk0
        
            return math.sqrt(self.sigma1)
        else:
            try:
                raise ClassException()
            except ClassException, E:
                E.muException()            

    def getDataPriorGammaDistribution(self):
        
        alpha = 0.01
        beta = 0.01
        n0 = alpha * 2.
        S0 = 2. * beta / n0 
        
        m0 = 1. / math.pow(self.sigma0, 2.)
        
        m1 = m0 + self.n
        n1 = n0 + self.n
        Q = self.n * math.pow(self.sigma, 2.)
        n1S1 = n0 * S0 + Q + (m0 * self.n) / (m0 + self.n) * math.pow((self.mu - self.mu0), 2. )
        
        mu1 = (self.n * self.mu + m0 * self.mu0) / (m0 + self.n)
        return (m1,n1,n1S1,mu1)

def main():
    
    """
    for test purposes (calculations)
    params data is TEST data from TEXT Book [Bayes distribution as Tools]
    """
    params = [30, 5.11,2.14646997,5,2]
    probBasedSDObj = probBasedSDClass(params)
    
#    probBasedSDObj.setDataKnownSigma(params)    
    rt = probBasedSDObj.getDataPriorGammaDistribution()    
    print rt
    
    mtp = metropolisHastings(False,False)
    mtp.unknownDistributionDataSet(rt)
    #(m,sg) = mtp.startSimulation(5.0,5.0,10000)
    (m,sg) = mtp.mainroutine(5.0,5.0,10000)
    
    print m , sg
    
    
    #print probBasedSDObj.calcMu1()
    #print probBasedSDObj.calcSimga1()    

if __name__ == "__main__":
    main() 