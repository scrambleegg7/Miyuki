#coding: utf-8

# for Japanese corpus setting
import nltk
from nltk.corpus.reader import *
from nltk.corpus.reader.util import *
from nltk.text import Text

import sys, codecs

#sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
#sys.stdin = codecs.getreader('utf_8')(sys.stdin)

from kanji2byte import pp

def test():
    data = {u'テスト': {u'america':u'アメリカ',u'india':u'インド'}}

    print data
    print pp(data)

    
if __name__ == '__main__':            
    FILE = "C:\\Users\\hiromi\\Downloads\\gingatetsudono_yoru.txt"
    f = open(FILE)
    string = f.read() 
    
    print string


#jp_sent_tokenizer = nltk.RegexpTokenizer(u'[^　「」！？。]*[！？。]')
#jp_chartype_tokenizer = nltk.RegexpTokenizer(u'([ぁ-んー]+|[ァ-ンー]+|[\u4e00-\\u9FFF]+|[^ぁ-んァ-ンー\u4e00-\u9FFF]+)')

#ginga = PlaintextCorpusReader("C:\\Users\\hiromi\\Downloads\\", r'gingatetsudono_yoru.txt',
#                               encoding='utf-8',
#                               para_block_reader=read_line_block,
#                               sent_tokenizer=jp_sent_tokenizer)
                               #word_tokenizer=jp_chartype_tokenizer)

#print ginga.raw()