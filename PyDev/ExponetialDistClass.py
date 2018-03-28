#coding: utf-8

import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma
from scipy.stats import expon

class ExponetialDistClass(object):
    
    def __init__(self):
        
        pass
        
    def __enter__(self):
        
        pass
    def __exit(self):
        
        pass
        

    def exponGamma(self):
        
        z = np.array([])
        z = gamma.rvs(expon.rvs(scale=1),loc=0,scale=gamma.rvs(0.1,0,scale=1),size=10000)
        
        return z


def main():
    
    expObj = ExponetialDistClass()
    ret_x = expObj.exponGamma()
    zz = ret_x * 100
    
    myfunc = lambda mu, x : mu ** x / (math.exp(mu) * math.factorial(x))
    xx = [myfunc(yy, 3) for yy in zz]
    
    fg = plt.figure()
    ax11 = fg.add_subplot(221) 
    ax11.hist(zz, bins=50)
       
    ax12 = fg.add_subplot(222) 
    ax12.hist(xx, bins=50)
    
    ax21 = fg.add_subplot(223)
    ax21.plot(xx,"r-")
    
    ax22 = fg.add_subplot(224)
    ax22.plot(zz,"b-")
    
    plt.show()
    
    
if __name__ == "__main__":
    main()