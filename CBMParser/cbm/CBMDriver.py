#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-   

from Tokenizer import *
from MeCabAdapter import *
from GoDanConjugations import *
import exrex

PRINT_ANS = 1
DEBUG = 0

"""Description: CBMDriver is a unifying  class that handles control and instantiation 
of other classes to fully implement CBM."""
class CBMDriver:
    def __init__(self, Cr ,Cs, direction):
        self.EnabledPatterns=[]
        self.rb = ConstraintBase()
        self.Cr = Cr
        self.ConstraintRelevance = Tokenizer()
        self.ConstraintRelevance.LexCheck(Cr)
        self.CrSymbols = self.ConstraintRelevance.ExpressionSymbols
        self.CrRootVerb = self.ConstraintRelevance.verb

        self.Cs = Cs
        self.ConstraintSatisfaction = Tokenizer()
        self.ConstraintSatisfaction.LexCheck(Cs)
        self.CsSymbols = self.ConstraintSatisfaction.ExpressionSymbols
        self.CsRootVerb = self.ConstraintSatisfaction.verb
        self.genRuleSet(self.CrSymbols, direction)

        #List of satisfied constraints and offset parameters
        #Each entry in the dictionary contains a key (constraint) and a value as a list comprised as follows:
        #   1 or 0 for pass or fail respectively
        #   pattern_offset - how far in the constraint pattern was matching successful
        #   text_offset - how far in the string from the left is the mismatch located 
        self.checkList ={}
        
        self.ExceptionList=[]
        exceptions = self.csv_reader(open('exceptions.csv'))
        for i in exceptions:
            self.ExceptionList.append(i)
    def csv_reader(self, utf8_data, delimiter=',', **kwargs):
        csv_reader = csv.reader(utf8_data, delimiter=delimiter, **kwargs)
        for row in csv_reader:
            yield row

    """genRuleSet checks the rules or inv_rules dictionary based on the relevance condition 
    and returns the expected rule as satisfaction condition. Requires 2 parameters - the relevance condition
    RegEx and the desired conversion direction, i.e. keigo to regular (Option 2) or regular to keigo (Option 1)"""
    def genRuleSet(self, parse_pattern, conversion):
        if conversion==1:
            RuleMatch = 0
            for key, value in self.rb.rules.items(): #This sample code is for using the dictionary "rules"
                regex = re.compile(key)
                if DEBUG==1:
                    print (regex, value)
                m = regex.match(parse_pattern)
                if m is not None:
                    RuleMatch = 1
                    self.EnabledPatterns = value
            if RuleMatch == 0:
                print ("No applicable constraint ordered pair for regular to keigo form conversion.")
        elif conversion == 2:
            RuleMatch = 0
            for key, value in self.rb.inv_rules.items(): #This sample code is for using the reverse of the dictionary "rules"
                regex = re.compile(key)
                if DEBUG==1:
                    print (regex, value)
                m = regex.match(parse_pattern)
                if m is not None:
                    RuleMatch = 1
                    self.EnabledPatterns = [value]
            if RuleMatch == 0:
                print ("No applicable constraint ordered pair for keigo to regular form conversion.")                   
        else:
            print ("Please specify only either 1 (regular to keigo conversion ruleset) or 2 (keigo to regular conversion ruleset")
    
        """sub_re and partial_pattern_match both work together to identify
    from which position from 0 in the string, are the mismatches from left to right."""
    #Refer: http://code.activestate.com/recipes/475187-regular-expression-point-of-failure/
    def sub_re(self, pattern):
        for offset in range(len(pattern)+1,0,-1):
            try:
                re_obj = re.compile(pattern[:offset])
            except re.error: # syntax error in re part
                continue
            yield offset, re_obj
            
    def partial_pattern_match(self, pattern):
        #pattern='W'+pattern+'Y' #Add BOS/EOS markers
        good_pattern_offset = 0
        good_text_offset = 0
        for re_offset, re_obj in self.sub_re(pattern):
            match = re_obj.match(self.CsSymbols)
            if match:
                good_pattern_offset = re_offset
                good_text_offset = match.end()
                return good_pattern_offset, good_text_offset
        return good_pattern_offset, good_text_offset
    
    def ShowAnswer(self):
        answers = []
        for constraint in self.EnabledPatterns:
            values = list(exrex.generate(constraint))
            for value in values:
                answers.append(self.DecodeSymbols(value))
        return list(set(answers))
            

    def DecodeSymbols(self, symbols):
        answer=''
        #Segment each symbol and match to its corresponding character for printing.
        PosSymbols = re.findall(r'([A-V][0-9]{1,2}|X[0-9]{1,2})',symbols)
        for i in PosSymbols:
            if re.match(r'X[0-9]{1,2}',i):
                if i=='X1':
                    answer+=utoi(self.CrRootVerb)
                if i=='X2':
                    answer+=self.CrRootVerb
                if i=='X3':
                    answer+=self.CrRootVerb
                if i=='X4':
                    answer+=self.CrRootVerb
                if i=='X5':
                    answer+=utoryk(self.CrRootVerb)
                if i=='X6':
                    answer+=utoa(self.CrRootVerb)
                if i=='X7':
                    answer+=utoer(self.CrRootVerb)
                if i=='X8':
                    answer+=utoe(self.CrRootVerb)
                if i=='X9':
                    answer+=re.sub(r'る$', u'', self.CrRootVerb)
                if i=='X10':
                    answer+=re.sub(r'る$', u'', self.CrRootVerb)
            else:
                answer+=self.rb.inv_mapping[i].word
        return answer
    
    
    '''Verify: Checks if the answer matches a RegEx pattern designated to be as an acceptable answer.
    Returns True if there is a match. Returns false if otherwise.'''
    def Verify(self):
        for constraint in self.EnabledPatterns:
            pattern_offset = 0
            text_offset = 0
            pattern_offset, text_offset = self.partial_pattern_match(constraint) 
            #constraint can have multiple patterns that are acceptable.
            #The constraint length, +1 for EOS indicate a full constraint match.
            
            #+3 because of BOS, EOS and position at the end of the string. 
            #Since Oct 13, changed to +1 because of BOS/EOS marker removal.

            if len(constraint)+1==pattern_offset and self.CsRootVerb == self.CrRootVerb: #Ensure that the verb is still the same, unchanged.
                self.checkList[constraint]=["correct",pattern_offset,text_offset]
            else:
                self.checkList[constraint]=["wrong",pattern_offset,text_offset]
        
        #If there is a valid answer, we just keep that result, disregard the other attempted matches from the rules.
        filtered_dict = {k:v for (k,v) in self.checkList.items() if "correct" in v}
        if len(filtered_dict)!=0:
            self.checkList=filtered_dict
            return True
        else:
            return False
'''
    def PrintFeedback(self):
        ans = ', '.join(self.ShowAnswer())
        for key, value in self.checkList.items():
            if value[0]=="correct":
                print (key)
                if DEBUG == 1:
                    print ("OK")
                return ({"IsCorrect":1,
                         "Feedback":'OK'
                         })
            else:
                if DEBUG == 1:
                    print ("Expected constraint, pattern_offset", key, repr(value[1]))
                    print ("Good pattern", key[:value[1]])
                    print ("User answer", self.Cs)
                    print ('ー' * value[2] + '^')
                return ({"IsCorrect":0,
                         "Feedback":'Incorrect. Expected answer(s):'+ans
                         })
'''