#coding: utf-8

import numpy as np


class hmmClass(object):
    
    def __init__(self):
        self.pr = np.random.RandomState(9)
        self.startpr = self.pr.rand(3)
        self.startpr = self.startpr / sum(self.startpr)     
        self.tranmat = self.pr.rand(3,3)
        
        self.V = 300
        self.k = 6
        self.pi = np.random.dirichlet([1.] * self.k)
        self.B = np.ones((self.V,self.k)) / self.V
        self.alpha = []
        self.x = [1.,3.,5.,9.]
        self.N = len(self.x)
        self.alpha.append(self.pi * self.B[self.x[0]])
        
        print self.alpha

def main():
    hmmObj = hmmClass()

if __name__ == '__main__':
    main()