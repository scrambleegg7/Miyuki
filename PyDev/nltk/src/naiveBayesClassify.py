#coding: utf-8

import MeCab
import ngram
import nltk
import re
import numpy as np
from wordSens.wordSens import wordSensClass

def WordSensDic():
    wordObj = wordSensClass('J')
    wordObj.setFileName()
    dic = {}
    dic = wordObj.makeDictionary()
    return dic


class testClass(object):
    
    def __init__(self):
        self.rows = None
        self.rowlength = 0
        self.allwords = []
        self.sentences = []
        pass
    
    def readFile(self):
        FILE = "C:\\temp\\Twitter_.txt"
        f = open(FILE,'rU')
        lines = f.readlines()
        self.rows = lines[:1000] #up to 1000
        self.rowlength = len(lines)        
    
    def readrows(self):
        pos_ = ['形容詞', '形容動詞','感動詞','副詞','連体詞','名詞','動詞']
        regexp2 = re.compile(ur'(^[0-9A-Za-z_\-]+$)|(^[A-Za-z_\-]+$)|(^[A-Za-z]+$)',re.UNICODE)
        #words_ = []
        personalDic_ = {}
        wordSensDic_ = WordSensDic()
        
        t_ = MeCab.Tagger('-Ochasen')
        for row_ in self.rows:
            #print row_
            spwords_ = row_.split(',')
            for item_ in spwords_:
                res_ = regexp2.search(item_)
                if res_ != None:
                    personalname_ = item_
                    words_ = []
                    vals_ = []
                    continue
                encode_ = item_.encode('utf-8')
                node = t_.parseToNode(encode_)
                node = node.next
                while node:
                    fs_ = node.feature.split(",")
                    if fs_[0] in pos_:
                        word_ = (fs_[6] != '*' and fs_[6] or node.surface)
                        words_.append(word_)
                        try:
                            decode_ = node.surface.encode('cp932')
                            val_ = wordSensDic_[decode_]
                            vals_.append(val_)
                        except:
                            #print "err"
                            pass
                        
                    #    self.allwords.append(word_)
                    node = node.next
                try:
                    personalDic_[personalname_] = (words_,vals_)
                except:
                    pass
                
        return personalDic_
    
    def ngram(self):
        pos_ = ['形容詞', '形容動詞','感動詞','副詞','連体詞','名詞','動詞']
        regexp2 = re.compile(ur'(^[0-9A-Za-z_\-]+$)|(^[A-Za-z_\-]+$)|(^[A-Za-z]+$)|(\$)|(\#)',re.UNICODE)
        
        ngramwords_ = []
        
        
        for row_ in self.rows:
            #print row_
            spwords_ = row_.split(',')
            for item_ in spwords_:
                res_ = regexp2.search(item_)
                if res_ != None:
                    personalname_ = item_
                    words_ = []
                    vals_ = []
                    continue
                
                self.sentences.append(item_)
                decode_ = item_.decode('utf-8')
                G = ngram.NGram(decode_,N=2)
                gg_ = [gg for gg in G.ngrams(G.pad(decode_)) if regexp2.search(gg) == None]
                ngramwords_.extend(gg_)    
        return ngramwords_
    
    def bayestrain(self):
        pos_ = ['形容詞', '形容動詞','感動詞','副詞','連体詞','名詞','動詞']
        regexp2 = re.compile(ur'(^[0-9A-Za-z_\-]+$)|(^[A-Za-z_\-]+$)|(^[A-Za-z]+$)|(\$)',re.UNICODE)
        personalDic_ = {}
        
        t_ = MeCab.Tagger('-Ochasen')
        for row_ in self.rows:
            #print row_
            spwords_ = row_.split(',')
            for item_ in spwords_:
                encode_ = item_.encode('utf-8')
                node = t_.parseToNode(encode_)
                node = node.next
                while node:
                    fs_ = node.feature.split(",")
                    try:
                        decode_ = node.surface.encode('cp932')
                        #print node.surface
                    except:
                        pass
                        
                    #    self.allwords.append(word_)
                    node = node.next
                
        return personalDic_
    
    def ngramCompare(self):
        
        t = 0
        for idx1,s1 in enumerate(self.sentences[:-1]):
            
            for idx2,s2 in enumerate(self.sentences[t+1:]):
                ratio_ = ngram.NGram.compare(s1,s2)
                if ratio_ == 0.0 or ratio_ == 1.0:
                    continue
                if ratio_ > 0.4:
                    print "[",ratio_,"]"
                    print "s1:%s,s2:%s\n" % (s1,s2)
            t += 2
            
    def morph(self,document):
        pass
    
    def process(self):
        
        self.readFile()
        print self.rowlength
        words_ = self.ngram()
        self.ngramCompare()
        """
        for k,(w,v) in dic_.iteritems():
            
            sum_ = np.sum(v)
            if sum_ > 0.1:
                print "[",k,"]"
                print "total feeling ratio:%1.6f" % sum_
                for w_ in w:
                    print w_
            #for v_ in v:
            #    print v_
        """    
        #allwords_ = [w_ for (w,v) in dic_.itervalues() for w_ in w]
        wordFreq_ = nltk.FreqDist(words_)
        wordFreq_.tabulate(10)
        text_ = nltk.Text(words_)
        text_.collocations()
        #wordFreq_.plot(50,cumulative=True)
        #for k in wordFreq_.keys()[:50]:
        #s    print k
        
def main():
    testObj = testClass()
    testObj.process()
    
    print "program end:"
    
if __name__ == '__main__':
    main()