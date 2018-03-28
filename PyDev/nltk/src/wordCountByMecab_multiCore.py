#coding: utf-8


from multiprocessing import Pool
import MeCab, os
import csv
import re
import codecs
from time import time

from kanji2byte import pp

def fileRead(FILENAME):
    
    f = open(FILENAME,'rU')
    lines_ = f.readlines()
    rowlength = len(lines_)
    return lines_

def fileReadShiftJis(FILENAME):
    
    text = codecs.open(FILENAME, 'r', 'shift-jis').read()
    print text
    return text

def cleanup(fhandler):
    
    string_ = []
    
    reg_mention_ = re.compile(r'@\w+')
    reg_url_ = re.compile(r'http://[\w./?=&#+\-]+')
    for wstring_ in fhandler:
        for w_ in wstring_:
            w_ = reg_mention_.sub('',w_)
            w_ = reg_url_.sub('',w_)
            #print w_
            if w_:
                string_.append(w_)
    
    return string_
            

def count_word(stringList):
    dict={}
    list=[]
    t = MeCab.Tagger()
    
    #print stringList
    
    for s_ in stringList:
        node = t.parseToNode(s_)
        while node:
            if node.feature.split(",")[0] == "名詞":
                print node.surface
                if node.surface in dict:
                    dict[node.surface] += 1
                else:
                    dict[node.surface] = 1
            node = node.next
    #登場回数が多い単語順にソート
    for word, count in sorted(dict.items(), key=lambda x:x[1], reverse=True):
        list.append(str(count)+"\t"+word)
    return list
    
def printList(plist):
    
    for p_ in plist:
        print p_
    
if __name__ == '__main__':
    #FILE = "C:\\Users\\hiromi\\Downloads\\gingatetsudono_yoru.txt"
    FILE = "C:\\temp\\Twitter_.txt"
    
    #1コアによる処理
    """
    t = time()
    count_list=[]
    for i in xrange(0, 100):
        count_list.append(count_word(FILE))
    single_time = time()-t
    print "single: %f sec" % (single_time)
    """
    #複数コアによる処理
    t = time()
    #Pool(None)は自動的にcpu_count()の値が入る
    p = Pool()
    count_list=[]
    file_list = []
    fhd_ = fileRead(FILE)
    string_ = cleanup(fhd_)
    count_list = p.map(count_word, string_)
    multi_time = time()-t
    print "multi working time: %f sec" % (multi_time)
    
    #print "single: %f sec" % (single_time)