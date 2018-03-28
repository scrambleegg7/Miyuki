#coding: utf-8
from __future__ import division


import math
import sys
import logging

class ClassLogging(object):
    
    def __init__(self,pgname):
        
        self.filename = "c:\\temp\\%s.log" % pgname
        logging.basicConfig(filename=self.filename,level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        
    def __enter__(self):
        
        pass
    
    def logging(self,msg):
        logging.debug(msg)
