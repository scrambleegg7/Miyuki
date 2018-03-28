#coding: utf-8
import urllib
from time import time
from time import sleep
from readCSVF import readFileCSVEXCEL 
from xml.etree.ElementTree import parse
from pygeocoder import Geocoder

start = time()

def adr2geo(adr):
    #api = "http://www.geocoding.jp/api/?v=1.1&q=%s" % (urllib.quote(adr.encode('utf-8')))
    #api = "https://maps.googleapis.com/maps/api/geocode/xml?%s" % (urllib.quote(adr.encode('utf-8')))
    #xml = parse(urllib.urlopen(api)).getroot()
    
    try:
        results = Geocoder.geocode(adr.encode('utf-8'))
        lat = results[0].coordinates[0]
        lng = results[0].coordinates[1]
    except:
        
        return (0.0,0.0)
    return (float(lat), float(lng))
 
def fileRead(f):
    try:
        fh_ = readFileCSVEXCEL(f,True)
    except:
        print "IOError"
        fh_ = None
    return fh_

def integrate(fh_k_,fh_n_):
    client ={}
    client_ = {}
    #monthly = {}
    for rr in fh_k_:
        client[int(rr[1])] = rr[21].decode('cp932')
        #print rr[1],rr[21].decode('cp932')
    
    if fh_n_:
        for geo_ in fh_n_:
            if client.get(int(geo_[0])):
                print "obsolet from dictionary",client.pop(int(geo_[0]))
    return client

def process():
    f1 = "\\\\EMSCR01\ReceptyN\\TEXT\\KANJA_List.txt"
#     f1 = "\\\\EMSCR01\ReceptyN\\TEXT\\JA_List.txt"
    f2 = "c:\\temp\\geocoder.txt"
    fh_k_ = fileRead(f1)
    fh_n_ = fileRead(f2)
    mclient_ = integrate(fh_k_,fh_n_)
    
    rowsize_ = float(len(mclient_))
    print "Total Size:%d" % rowsize_
    myidx_ = 0.0
    for k_,v_ in mclient_.iteritems():
        if v_:
            #print myidx_,k_,v_
            myidx_ += 1.0
            lat_,lng_ = adr2geo(v_)
            if lat_ != 0.0 and lng_ != 0.0:
                f = open('c:\\temp\\geocoder.txt', 'a')
                processratio_ = float(myidx_/rowsize_ * 100)
                print "%d %d %3.4f %3.4f  completed:%2.2f " % (myidx_,k_,lat_,lng_,processratio_)
                elapsed()
                sleep(5)
                string_ = str(k_) + ',' + str(lat_) + ',' + str(lng_) + '\n'
                f.write(string_)
                f.close()

def elapsed():
    print "elasped: %.3fs" % (time() - start)
    
def main():
    print "Process Starting"
    process()
    elapsed()
    print "Process End"
    
if __name__ == "__main__":
    main()