#coding:utf-8

import nltk
import re, os

symbols = ["''","'", '"', '`', '``', '.', ',', '-', '!', '?', ':', ';', '(', ')']
stopwords = nltk.corpus.stopwords.words('english')

def read(d):
    files = os.listdir(d)
    files = filter(lambda x: x != 'cmds', files) 
    xs = ''
    for file in files:
        
        with open(d + file,'rU') as con:
            msg = con.readlines()
            r = re.compiler(r'\n')
            #print msg
            firstblank = msg.index("\n")
            msg = msg[(firstblank+1):]
        #f = open(d + file)
        #string = f.read()
            xs = ''.join(msg)
    
    return xs
    
def tokenize(s):
    tokens = nltk.word_tokenize(s)
    #print tokens
    text = nltk.Text(tokens)
    print "sum of tokens:   %d" % len(tokens)
    tokens_l = [w.lower() for w in tokens]
    print "distinct tokens: %d" % len(set(tokens_l))
    
    punctuation = re.compile(r'[-+.?!,":;()|0-9/<>=$&%#~@\[\]]')
    p = re.compile(r'face')
    
    new_tokens = [punctuation.sub("",w) for w in tokens_l]
    fd = nltk.FreqDist(w for w in new_tokens if w not in symbols + stopwords)
    
    #print text.concordance('zzzz',lines=10)
    
    return fd

def main():
    DIR = []
    DIR.append("C:\\temp\\spam_corpus\\spam\\")
    #DIR.append("C:\\temp\\spam_corpus\\spam_2\\")
    #DIR.append("C:\\temp\\spam_corpus\\easy_ham\\")
    #DIR.append("C:\\temp\\spam_corpus\\easy_ham_2\\")
    #DIR.append("C:\\temp\\spam_corpus\\hard_ham\\")
    for dirct in DIR:
        print "*** ", dirct
        string = read(dirct)
        fd = tokenize(string)
        print "Email top 50 words from messages."
        print fd.keys()[:50]
        print "\n"

    #spam top 50 words
    #fd.plot(50,cumulative=True)

if __name__ == '__main__':            
    main()
    

