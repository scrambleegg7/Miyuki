#coding: utf-8

import sys
import datetime
import re
import numpy as np

from CacheDBClass import CacheDB

class weeklyDrugClass(object):
    
    attributes = ['drugCode','drugName','freq']
    
    def __init__(self):
        pass
        
    def __enter__(self):
        pass
        
    def __exit__(self):
        pass

    def dataSelect1(self):
        #print "dataSelect1"
        sqlstat = 'select drugCode,drugName,freq from weeklydrug' 
        print sqlstat 
        return sqlstat 

    