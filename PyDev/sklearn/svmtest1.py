#coding: utf-8

import numpy as np
import pickle
from sklearn.svm import SVC
from sklearn import datasets
from sklearn.externals import joblib
from scipy.stats import norm,bernoulli

def datagen():
    data = norm.rvs(0,1,size=(4,4))
    return data

def irisfit():
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    return (X,y)
    
def main():
    
    data = datagen()
    X = data[:,:-1]
    y = data[:,-1]
    X1 = X[0:3]
    y1 = y[0:3]
    print "X\n",X
    print "y\n",y
    print "X0\n",X[3]
    print "y0\n",y[3]
    print "X1\n",X1
    print "y1\n",y1
    #X,y = irisfit()
    
    clf = SVC()
    clf.fit(X1,y1)
    #joblib.dump(clf,'data.dump')
    #Xtest = norm.rvs(0,1,size=(7,6))
    t1 = clf.predict(X)
    
    print "result\n", t1
    print "score\n", clf.score(X,y)
    
if __name__ == '__main__':
    main()
    


