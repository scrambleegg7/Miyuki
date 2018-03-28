#coding: utf-8

import numpy as np
from scipy.stats import norm
import sys,traceback
import matplotlib.pyplot as plt


class bayesRegression(object):

    def debug(self,msg):
        if self.debugsw:
            print(msg)
    
    def __init__(self,x,t):
        self.x = x
        self.t = t
        self.wv = None
        
        """
        debug sw on = print 
        """
        self.debugsw = True
        self.gausw = True
        self.bayesw = True
        
        self.debug(self.x)
        self.debug(self.t)
        
    def __enter__(self):
        self.startCalculation()
        self.depict(self.x.min(),self.x.max(),0.01)
    
    def __exit__(self, type, value, traceback):
        pass
    
    def startCalculation(self):
        print "Bayes Regression Start "
        if self.bayesw:
            self.wv = self.sigmaAndmu()
        else:
            self.wv = self.w()
        self.debug([ww for ww in self.wv])
    
    def depict(self,xstart,xend,step):
        xlist = np.arange(xstart,xend,step)
        
        if self.gausw:
            ylist = [np.dot(self.wv, self.PhiGauss(x)) for x in xlist]
        elif self.bayesw:
            ylist = [np.dot(self.wv, self.PhiGauss(x)) for x in xlist]
        else:
            ylist = [self.f(self.wv, x) for x in xlist]

        plt.plot(xlist,ylist)
        plt.plot(self.x,self.t,'o')
        plt.show()
    
    def PhiGauss(self,x):
        s = 0.1 # width of gauss base
        #return np.append(1, np.exp(-(x - np.arange(0, 1 + s, s)) ** 2 / (2 * s * s)))
        return np.append(1, np.exp(-(x - np.arange(0, 1 + s, s)) ** 2 / (2 * s * s)))
    
    def Phi(self,x):    
        return [1, x, x ** 2, x ** 3]
        #return [1, x, x ** 2, x ** 3, x ** 4, x ** 5]
            
    def mu(self,x):
        pass
    
    def sigmaAndmu(self):
        alpha = 0.1
        beta = 0.9
        
        phi = self.phiMatrix()
        self.debug(phi)
        
        sigma_N = np.linalg.inv(alpha * np.identity(phi.shape[1]) + beta * np.dot(phi.T, phi))
        mu_N = beta * np.dot(sigma_N, np.dot(phi.T, self.t))
        
        self.debug(sigma_N)
        self.debug(mu_N)
        
        return mu_N
    
    def w(self):
        phi = self.phiMatrix()
        self.debug(phi)
        if self.gausw:
            return np.linalg.solve(np.dot(phi.T, phi), np.dot(phi.T, self.t))
        else:
            return np.dot(np.linalg.inv(np.dot(phi.T, phi)), np.dot(phi.T,self.t))
         
    def phiMatrix(self):
        if self.gausw:
            return np.array([self.PhiGauss(X) for X in self.x])
        elif self.bayesw:
            return np.array([self.PhiGauss(X) for X in self.x])
        else:
            return np.array([self.Phi(X) for X in self.x])
    
    def f(self,w,x):
        return w[0] + w[1] * x + w[2] * (x ** 2) + w[3] * (x ** 3)
        #return w[0] + w[1] * x + w[2] * (x ** 2) + w[3] * (x ** 3) + + w[4] * (x ** 4) + w[5] * (x ** 5)
    
def main():
    """
    for checking 
    """
    #X = np.array([0.02, 0.12, 0.19, 0.27, 0.42, 0.51, 0.64, 0.84, 0.88, 0.99])
    #t = np.array([0.05, 0.87, 0.94, 0.92, 0.54, -0.11, -0.78, -0.89, -0.79, -0.04])
    
    X = norm.rvs(0,1,size=20)
    t = norm.rvs(0,1,size=20)
    
    bayesObj = bayesRegression(X,t)
    try:
        with bayesObj:
            print "TEST is Finished!!"
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