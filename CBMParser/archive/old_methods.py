#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-   

from MeCabAdapter import *
from Tokenizer import *
import re

DEBUG = 0

class GetExpression:
    def __init__(self, KeigoString):
        #Initialize data required by this class
        self.t = Tokenizer(KeigoString)
        self.t.SentenceTokenizer()
        self.rb = ConstraintBase()
        #Class data stores
        self.targets=[]


    #def Deduplicate(self, seq):
    #    seen = set()
    #    seen_add = seen.add
    #    return [x for x in seq if not (x in seen or seen_add(x))]
    
    #def DelimSep(self, seq, sep):
    #    return [list(y) for x, y in itertools.groupby(seq, lambda z: z == sep) if not x]