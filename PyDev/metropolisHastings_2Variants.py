#coding:utf-8

import math
from random import seed
from random import random
from random import uniform
import numpy as np
import matplotlib.pyplot as plt


def met(f,start=1.0,delta=2.0,burn_in=100,seed=1):

    iter = _met(f,start,delta,seed)
    for i,val in enumerate(iter):
        #print i
        if i > burn_in:
            #yield val
            break
    
    for val in iter:
        yield val


def _met(f,start,delta,sd):
    
    seed(sd)
    init_x1 = start
    init_x2 = start
    init_fx = f(init_x1,init_x2)
    
    
    p_x1,p_x2,p_fx = 0.,0.,0.
     
    for j in range(1,1000):
        p_x1 = init_x1 + uniform(-delta,delta)
        p_x2 = init_x2 + uniform(-delta,delta)
        p_fx = f(p_x1,p_x2)
    
        ratio = p_fx / init_fx
        if ratio > 1. or ratio > random():
            init_x1,init_x2,init_fx = p_x1,p_x2,p_fx
            yield p_x1,p_x2,p_fx
        else:
            yield init_x1,init_x2,init_fx


def main():
    
    f = lambda x1,x2 : x1 + x2
    #f = lambda x1,x2: math.exp(-x1 * x2 / 10.0)
    xb1 = []
    xb2 = []
    fxb = []
    
    for x1,x2,fx in met(f):
        xb1.append(x1)
        xb2.append(x2)
        fxb.append(fx)
        
    tx = range(1,len(fxb)+1)
    print len(xb1)
    plt.plot(xb1,xb2,"bo")
    plt.plot(tx,fxb)
    plt.show()
    
    
    
    
if __name__ == '__main__':
    main()