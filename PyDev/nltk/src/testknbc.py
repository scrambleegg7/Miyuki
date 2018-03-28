#coding: utf-8

from knbc import *
from nltk.corpus.util import LazyCorpusLoader
import re

class kfactory(object):
    
    def __init__(self):
        knbc = LazyCorpusLoader('C:\\Users\\hiromi\\AppData\\Roaming\\nltk_data\\corpora', KNBCorpusReader, r'.*/KN.*', encoding='euc-jp')
        print knbc.fileids()
        #print ''.join( knbc.words()[:100] )
        self.kfactory = knbc
    
    def knbc(self):
        return self.kfactory
        

def init():
    #root = nltk.data.find('C:\Users\hiromi\AppData\Roaming\nltk_data')
    #fileids = [f for f in find_corpus_fileids(FileSystemPathPointer(root), ".*") if re.search(r"\d\-\d\-[\d]+\-[\d]+", f)]
    kfObj = kfactory()
    
def testprint(knbc):
    pass
    
    
def main():
    init()
    
if __name__ == '__main__':
    main()