#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-    
import re
from MeCabAdapter import *
from Rules import *
from Word import *
from operator import itemgetter

DEBUG = 0

"""Tokenizer: Class designed for implementing search of acceptable lexicons in a sentence and 
    checking for the presence of target expressions for CBM in a sentence."""
class Tokenizer():
    def __init__(self):
        self.rb = ConstraintBase()
        
        self.SentenceSymbols='' #Parser grammar symbols
        self.ExpressionSymbols='' #Parser grammar symbols
        self.verb='' #Verb in keigo expression, dictionary form
        self.targets=[] #List of target expressions for CBM checking

    """SymToChar: Converts string symbols back to their characters."""
    def SymToChar(self, StringSymbols):
        ConSym=''
        ParsedSymbols = re.findall(r'(Z[0-9]{1,3}|[A-V][0-9]{1,2}|X[0-9]{1,2}(-[0-9]+){0,1})', StringSymbols)
        SelList = [x[0] for x in ParsedSymbols]
        for i in SelList:
            if i in self.rb.inv_mapping:
                ConSym+= re.sub(re.compile(i),self.SentenceSymbols,self.rb.inv_mapping[i].word)
                #symbols=symbols.replace(i,self.rb.inv_mapping[i].word)
            elif i in self.rb.inv_UnkDict:
                ConSym+= re.sub(re.compile(i),self.SentenceSymbols,self.rb.inv_UnkDict[i].word)
                #symbols=symbols.replace(i,self.rb.inv_UnkDict[i].word)
        return(ConSym)

    """LocateTargets: Gets the start and end position, plus the matched symbols in a sentence that a constraint 
    applies to. Each result is a tuple, stored in a list."""
    def LocateTargets(self, conversion):
        if conversion=='2':
            if DEBUG==1:
                print (self.SentenceSymbols)
            for s in self.rb.inv_rules.keys():
                regex = re.sub(r'(X[0-9]{1,2})',r'\1(-[0-9]+){0,1}', s)
                p = re.compile(regex)
                for m in p.finditer(self.SentenceSymbols):
                    self.targets.append([m.start(), m.end(), m.group()])
        elif conversion=='1':
            if DEBUG==1:
                print (self.SentenceSymbols)
            for s in self.rb.rules.keys():
                regex = re.sub(r'(X[0-9]{1,2})',r'\1(-[0-9]+){0,1}', s)
                p = re.compile(regex)
                for m in p.finditer(self.SentenceSymbols):
                    self.targets.append([m.start(), m.end(), m.group()])
        else:
            print ("Please specify only either 1 (regular to keigo conversion ruleset) or 2 (keigo to regular conversion ruleset")
    
                
    """SentenceTokenizer: Parses a string to identify each POS and map them to representative symbols in the mappings dictionary.
    The difference of this method to LexCheck(), is that we prioritize based on the MeCab result precendence (top preferred)
    and the ability to parse everything, irrespective of the verb."""
    def SentenceTokenizer(self, SentenceString):
        #Mecab Init
        MeCabResults = Parser(SentenceString)
        MeCabResults.parse(self.rb.NBEST)
        counter=1
        
        ##########################
        #Temporary Variable Stores
        CandidateExpressions = []#List containing parse symbols (expression), each entry a result set from MeCab.
        UnkStore = [] #List storing the unks according to result precendence from MeCab.
        inv_UnkStore = []
        inv_mappingStore = []
        ##########################
        expression=''
        while counter <= self.rb.NBEST:
            expression=''
            UnkCounter=0
            VerbIdxCounter=0
            inv_mapping_cand={v: k for k, v in self.rb.mapping.items()}
            Unk_Dict_cand={}
            inv_Unk_Dict_cand={}
            results = MeCabResults.all
            for i in results[counter-1]:
                if DEBUG  ==1:
                    print (i.word)
                    
                #Note to the developer:
                #For 連体形, we handle it under the same symbol if the verb form is the same. This is applicable to VERBS ONLY.
                #This has been done for 使う、食べる、使える type of verbs.
                
                #For verbs like 使い
                if i.pos=='動詞' and i.spos1=='一般' and '五段' in i.goDan and \
                i.conjugation=='連用形-一般' and i.word not in (x[0] for x in self.rb.ExceptionList):
                    expression+='X1-'+str(VerbIdxCounter)
                    inv_mapping_cand['X1-'+str(VerbIdxCounter)]=i
                    VerbIdxCounter+=1
                elif i.pos=='名詞' and i.spos2=='サ変可能':
                    expression+='X2-'+str(VerbIdxCounter)
                    inv_mapping_cand['X2-'+str(VerbIdxCounter)]=i
                    VerbIdxCounter+=1
                #For verbs like 食べる
                elif i.pos=='動詞'  and i.spos1=='一般' and '一段' in i.goDan and \
                (i.conjugation=='終止形-一般' or i.conjugation=='連体形-一般') and \
                i.word not in (x[0] for x in self.rb.ExceptionList):
                    expression+='X3-'+str(VerbIdxCounter)
                    inv_mapping_cand['X3-'+str(VerbIdxCounter)]=i
                    VerbIdxCounter+=1
                #For verbs like 使う
                elif i.pos=='動詞'  and i.spos1=='一般' and '五段' in i.goDan and \
                (i.conjugation=='終止形-一般' or i.conjugation=='連体形-一般'):
                    expression+='X4-'+str(VerbIdxCounter)
                    inv_mapping_cand['X4-'+str(VerbIdxCounter)]=i
                    VerbIdxCounter+=1
                #For verbs like 使った, the 使っ portion
                elif i.pos=='動詞'  and i.spos1=='一般' and '五段' in i.goDan and \
                i.conjugation=='連用形-促音便':
                    expression+='X5-'+str(VerbIdxCounter)
                    inv_mapping_cand['X5-'+str(VerbIdxCounter)]=i
                    VerbIdxCounter+=1
                #For verbs like 使わ
                elif i.pos=='動詞'  and i.spos1=='一般' and '五段' in i.goDan and \
                i.conjugation=='未然形-一般':
                    expression+='X6-'+str(VerbIdxCounter)
                    inv_mapping_cand['X6-'+str(VerbIdxCounter)]=i
                    VerbIdxCounter+=1
                #For verbs like 使える
                elif i.pos=='動詞'  and i.spos1=='一般' and \
                (i.conjugation=='終止形-一般' or i.conjugation=='連体形-一般') and \
                i.word in (x[0] for x in self.rb.ExceptionList):
                    expression+='X7-'+str(VerbIdxCounter)
                    inv_mapping_cand['X7-'+str(VerbIdxCounter)]=i
                    VerbIdxCounter+=1
                #For verbs like 使え
                elif i.pos=='動詞'  and i.spos1=='一般' and \
                i.conjugation=='連用形-一般' and \
                i.word in (x[0] for x in self.rb.ExceptionList):
                    expression+='X8-'+str(VerbIdxCounter)
                    inv_mapping_cand['X8-'+str(VerbIdxCounter)]=i
                    VerbIdxCounter+=1
                #For verbs like 食べ
                elif i.pos=='動詞' and i.spos1=='一般' and '一段' in i.goDan and \
                i.conjugation=='連用形-一般' and \
                i.word not in (x[0] for x in self.rb.ExceptionList):
                    expression+='X9-'+str(VerbIdxCounter)
                    inv_mapping_cand['X9-'+str(VerbIdxCounter)]=i
                    VerbIdxCounter+=1
                #For verbs like 食べ+られる（可能形）
                elif i.pos=='動詞' and i.spos1=='一般' and '一段' in i.goDan and \
                i.conjugation=='未然形-一般' and \
                i.word not in (x[0] for x in self.rb.ExceptionList):
                    expression+='X10-'+str(VerbIdxCounter)
                    inv_mapping_cand['X10-'+str(VerbIdxCounter)]=i
                    VerbIdxCounter+=1
                else:
                    if i in self.rb.mapping:
                        expression+=self.rb.mapping[i]
                    else:
                        SymbolAssignment='Z'+str(UnkCounter)
                        expression+=SymbolAssignment
                        Unk_Dict_cand[i] = SymbolAssignment
                        inv_Unk_Dict_cand[SymbolAssignment] = i
                        UnkCounter+=1
            counter+=1
            CandidateExpressions.append(expression)
            UnkStore.append(Unk_Dict_cand)
            inv_UnkStore.append(inv_Unk_Dict_cand)
            inv_mappingStore.append(inv_mapping_cand)

        temp = [[idx, len(val)] for idx, val in enumerate(UnkStore)]
        #ParseSolution is a List - Index of Result, Count of Unks of that result
        #Get the result with the least nunber of unk tokens.
        ParseSolution = min(temp, key=itemgetter(1,0))
        
        #Store the results:
        self.SentenceSymbols=CandidateExpressions[ParseSolution[0]]
        self.rb.UnkDict = UnkStore[ParseSolution[0]]
        self.rb.inv_UnkDict = inv_UnkStore[ParseSolution[0]]
        self.rb.inv_mapping = inv_mappingStore[ParseSolution[0]]
        
        if counter>self.rb.NBEST:
            counter-=1
        if DEBUG ==1:
            print (self.symbols)
    
    """LexCheck: Check each parsed result if each POS is in the lexicon of the defined CBM patterns
    and convert them to their assigned internal symbols."""
    def LexCheck(self, VerbString):
        #Mecab Init
        MeCabResults = Parser(VerbString)
        MeCabResults.parse(self.rb.NBEST)
        HasUnk=0 #Indicator whether a full parse to acceptable symbols has been made
        counter=1
        expression=''     
        while 'X' not in expression and counter <= self.rb.NBEST:
            expression=''
            UnkCounter=0
            results = MeCabResults.all
            for i in results[counter-1]:
                if DEBUG  ==1:
                    print (i.word)
                    
                #Note to the developer:
                #For 連体形, we handle it under the same symbol if the verb form is the same. This is applicable to VERBS ONLY.
                #This has been done for 使う、食べる、使える type of verbs.
                
                #For verbs like 使い
                if i.pos=='動詞' and i.spos1=='一般' and '五段' in i.goDan and \
                i.conjugation=='連用形-一般' and i.word not in (x[0] for x in self.rb.ExceptionList):
                    expression+='X1'
                    self.verb = i.dictForm
                elif i.pos=='名詞' and i.spos2=='サ変可能':
                    expression+='X2'
                    self.verb = i.word
                #For verbs like 食べる
                elif i.pos=='動詞'  and i.spos1=='一般' and '一段' in i.goDan and \
                (i.conjugation=='終止形-一般' or i.conjugation=='連体形-一般') and \
                i.word not in (x[0] for x in self.rb.ExceptionList):
                    expression+='X3'
                    self.verb = i.dictForm
                #For verbs like 使う
                elif i.pos=='動詞'  and i.spos1=='一般' and '五段' in i.goDan and \
                (i.conjugation=='終止形-一般' or i.conjugation=='連体形-一般'):
                    expression+='X4'
                    self.verb = i.dictForm
                #For verbs like 使った, the 使っ portion
                elif i.pos=='動詞'  and i.spos1=='一般' and '五段' in i.goDan and \
                i.conjugation=='連用形-促音便':
                    expression+='X5'
                    self.verb = i.dictForm
                #For verbs like 使わ
                elif i.pos=='動詞'  and i.spos1=='一般' and '五段' in i.goDan and \
                i.conjugation=='未然形-一般':
                    expression+='X6'
                    self.verb = i.dictForm
                #For verbs like 使える
                elif i.pos=='動詞'  and i.spos1=='一般' and \
                (i.conjugation=='終止形-一般' or i.conjugation=='連体形-一般') and \
                i.word in (x[0] for x in self.rb.ExceptionList):
                    expression+='X7'
                    for x in self.rb.ExceptionList:
                        if i.word == x[0]:
                            self.verb = x[3]
                #For verbs like 使え
                elif i.pos=='動詞'  and i.spos1=='一般' and i.conjugation=='連用形-一般' and \
                i.word in (x[0] for x in self.rb.ExceptionList):
                    expression+='X8'
                    for x in self.rb.ExceptionList:
                        if i.word == x[0]:
                            self.verb = x[3]
                #For verbs like 食べ
                elif i.pos=='動詞' and i.spos1=='一般' and '一段' in i.goDan and \
                i.conjugation=='連用形-一般' and \
                i.word not in (x[0] for x in self.rb.ExceptionList):
                    expression+='X9'
                    self.verb = i.dictForm
                #For verbs like 食べ+られる（可能形）
                elif i.pos=='動詞' and i.spos1=='一般' and '一段' in i.goDan and \
                i.conjugation=='未然形-一般' and \
                i.word not in (x[0] for x in self.rb.ExceptionList):
                    expression+='X10'
                    self.verb = i.dictForm
                else:
                    if i in self.rb.mapping:
                        expression+=self.rb.mapping[i]
                    else:
                        SymbolAssignment='Z'+str(UnkCounter)
                        expression+=SymbolAssignment
                        self.rb.UnkDict[i] = SymbolAssignment
                        self.rb.inv_UnkDict[SymbolAssignment] = i
                        UnkCounter+=1
                        HasUnk=1
            #Checking if multiple strings are possibly in a string 
            #Refer to http://stackoverflow.com/questions/3389574/check-if-multiple-strings-exist-in-another-string
            VerbMarkers = ['X1','X2','X3','X4','X5','X6','X7','X8','X9','X10', 'X11']
            if HasUnk==0 and any (x in expression for x in VerbMarkers):
                pass
            else:
                counter+=1
        self.ExpressionSymbols=expression
        
        if counter>self.rb.NBEST:
            counter-=1
        if DEBUG ==1:
            print (self.symbols)
            
    @property
    def SentenceSymbols(self):
        return self.__SentenceSymbols
    @SentenceSymbols.setter
    def SentenceSymbols(self, SentenceSymbols):
        self.__SentenceSymbols = SentenceSymbols
    @property
    def ExpressionSymbols(self):
        return self.__ExpressionSymbols
    @ExpressionSymbols.setter
    def ExpressionSymbols(self, ExpressionSymbols):
        self.__ExpressionSymbols = ExpressionSymbols
    @property
    def verb(self):
        return self.__verb
    @verb.setter
    def verb(self, verb):
        self.__verb = verb
