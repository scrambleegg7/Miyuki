#coding: utf-8
import readCSVF
import matplotlib.pyplot as plt
import math
from MyDateClass import MyDateClass


def poisson(elist):
    mu = 0
    
    evt = {}
    sigma = sum(1 for x in elist)
    for x in elist:
        
        if x not in evt:
            evt[x] = 1
        else:
            evt[x] += 1    
    
    for m in evt:
        mu += m * evt[m]
        #print m,evt[m]
    mu = int(mu)/sigma
    std = math.sqrt(mu)
    print "mu:%10.2f std:%10.2f"  % (mu,std)
    print "99 confidence Interval :(low)%10.2f (high)%10.2f" % (mu-3*std, mu+3*std)
            
    return mu

def main():

    fdir = "C:\\Apache2.2\\htdocs\\PyDev\\"
    f = fdir + "mrs.csv"    
    print "reading file : %s " % f
    
    mObj = MyDateClass()
        
    fhd = readCSVF.readFileCSVEXCEL(f,True)
    rlist = list(fhd)
    tlist = []
    xlist = []
    mlist = range(13)
    oyyyymm = None
    msum = 0
    ymKey = {}
    for rr in rlist:
        t = mObj.setDate(rr[0])
        
        if mObj.strYYYYMM() not in ymKey:
           vlist = []
           evtlist = []
           vlist.append(int(rr[1]))
           vlist.append(1)
           evtlist.append(int(rr[1]))
           vlist.append(evtlist)
           ymKey[mObj.strYYYYMM()] = vlist 
        else:
           ul = ymKey[mObj.strYYYYMM()]
           ul[0] += int(rr[1])
           ul[1] += 1
           ul[2].append(int(rr[1])) 
           ymKey[mObj.strYYYYMM()] = ul
             
        tlist.append(t)
        xlist.append(rr[1])
    
    for x in ymKey:
        #print x,ymKey[x][0],ymKey[x][1],ymKey[x][0]/ymKey[x][1],ymKey[x][2]
        print "Target Date: %s" % x
        mu = poisson(ymKey[x][2])

#    fig = plt.figure()
#    ax1 = fig.add_subplot(111)
#    ax1.plot(tlist,xlist,'o',color='r')
    #plt.show()

if __name__ == "__main__":
    main()