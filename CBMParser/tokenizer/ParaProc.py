#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-   

from Tokenizer import *
import re
import nltk

"""ParagraphPreprocessor: Class intended to splice paragraphs into sentences and 
    locate the target expression in each sentence. Requires a paragraph (string)."""
class ParagraphPreprocessor():
    def __init__(self):
        self.pkMap={}
        self.MarkedSentences = []

    """MarkExpressions: Marks each target expression with an x-editable HTML tag."""
    def MarkExpressions(self,paragraph,conversion):
        sentences = []
        delimiters = nltk.RegexpTokenizer(u'[^！？。]*[！？。]')
        SentenceList = delimiters.tokenize(paragraph)
        for s in SentenceList:
            s.strip()
            sentences.append(s)        

        counter = 1
        for sentence in sentences:
            t = Tokenizer()
            t.SentenceTokenizer(sentence)
            t.LocateTargets(conversion)
            CBMTargets = t.targets
            for CBMTarget in CBMTargets:
                StartTag='<span id="input'+str(counter)+'" class="label label-warning">'+str(counter)+\
                '</span><a href="#" id="vb" data-pk="'+str(counter)+'" data-url="/ConstraintCheck">'
                
                EndTag = '</a>'
                
                self.pkMap[counter]=t.SymToChar(CBMTarget[2])
                
                processed = t.SymToChar(t.SentenceSymbols[:CBMTarget[0]])+\
                StartTag+t.SymToChar(CBMTarget[2])+\
                EndTag+t.SymToChar(t.SentenceSymbols[CBMTarget[1]:])
                self.MarkedSentences.append(processed)
                counter+=1

