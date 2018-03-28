#coding: utf-8

import re

class StringClass(object):
    
    def __init__(self,data):
        #self.uString = None
        self.uString = data
    
    def __del__(self):
        pass
    
    def cp932Converter(self):
        """
        if any non numeric or character is found in the word,
        the input data is automatically converted to cp932 (unicode) for saving data 
        on SQL
        """
        regexp = re.compile(r'^[0-9A-Za-z]+$')
        result = regexp.search(self.uString)
        if result != None:
            #print "-- num char only"
            return self.uString
        else:
            #print "-- Non num char "
            return self.uString.decode('cp932')
    