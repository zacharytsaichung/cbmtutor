#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-   

from MeCabAdapter import Parser
import csv
import re

DEBUG=0
"""VerbAnalyzer: Checks the form of the verb to be converted to keigo, and returns the index of the relevant honorific polite 
    expression constraint in its equivalent form."""
class VerbAnalyzer:
    def __init__(self, verb):
        self.MeCabResult = Parser(verb)
        self.MeCabResult.parse()
        
        #Verb Properties
        self.HasMasu=0    #マス助動詞
        self.HasMasuRYK=0 #マス助動詞, 連用形-一般
        self.HasMasuMZN=0 #マス助動詞, 未然形-一般
        self.HasTa=0      #タ助動詞 
        self.HasNaiRYK=0  #ナイ助動詞, 連用形-一般
        self.HasNai=0     #ナイ助動詞
        self.HasTe=0      #テ助詞
        self.IsPotential=0
        self.HasIru=0
        self.IsJapVerb=0
        self.ExceptionList=[]
        exceptions = self.csv_reader(open('exceptions.csv'))
        for i in exceptions:
            self.ExceptionList.append(i)
    def csv_reader(self, utf8_data, delimiter=',', **kwargs):
        csv_reader = csv.reader(utf8_data, delimiter=delimiter, **kwargs)
        for row in csv_reader:
            for cell in row:
                yield cell
                
    def AnalyzeVerb(self):
        #print (self.ExceptionList)
        AllPOS = self.MeCabResult.all
        for i in AllPOS[0]:
            for j in self.ExceptionList:
                if j==i.word or j==i.dictForm: #This had to be done to force exact string matching.
                    self.IsPotential=1
            if i.WaKan=='和':
                self.IsJapVerb=1
            if i.goDan=='助動詞-ナイ':
                if i.word==i.dictForm:
                    self.HasNai=1
                else:
                    self.HasNai=1
                    self.HasNaiRYK=1
            if i.goDan=='助動詞-タ':
                self.HasTa=1
            if i.goDan=='助動詞-マス':
                if i.conjugation=='未然形-一般':
                    self.HasMasu=1
                    self.HasMasuMZN=1
                elif i.conjugation=='連用形-一般':
                    self.HasMasu=1
                    self.HasMasuRYK=1
                else:
                    self.HasMasu=1
            if i.pos=='助詞' and i.spos1=='接続助詞':
                self.HasTe=1
            if i.pos=='助詞' and i.dictForm=='いる':
                self.HasIru=1
    def VerbParameters(self):
        if self.IsPotential==0:
            if self.HasTe==0:
                if self.HasMasu==1: 
                    if self.HasMasuRYK==0 and self.HasMasuMZN==0:
                        if DEBUG==1:
                            print ("Masu present")
                        if self.IsJapVerb==1:
                            return [4,15]
                        else:
                            return [25,36]
                    elif self.HasMasuRYK==1 and self.HasTa==1:
                        if DEBUG==1:
                            print ("Masu past")
                        if self.IsJapVerb==1:
                            return [5]
                        else:
                            return [26]
                    elif self.HasMasuMZN==1 and self.HasTa==0:
                        if DEBUG==1:
                            print ("Masu present, negative")
                        if self.IsJapVerb==1:
                            return [6,16]
                        else:
                            return [27,37]
                    elif self.HasMasuMZN==1 and self.HasTa==1:
                        if DEBUG==1:
                            print ("Masu past, negative")
                        if self.IsJapVerb==1:
                            return [7,17]
                        else:
                            return [28,38]
                elif self.HasMasu==0:
                    if self.HasNai==1 and self.HasTa==0:
                        if DEBUG==1:
                            print ("Plain, negative")
                        if self.IsJapVerb==1:
                            return [8]
                        else:
                            return [29]
                    elif self.HasNai==1 and self.HasTa==1:
                        if DEBUG==1:
                            print ("plain, past, negative") 
                        if self.IsJapVerb==1:
                            return [9]
                        else:
                            return [30]
                    elif self.HasNai==0 and self.HasTa==1:
                        if DEBUG==1:
                            print ("plain, past")
                        if self.IsJapVerb==1:
                            return [2,14]
                        else:
                            return [23,35]
                    else:
                        if DEBUG==1:
                            print ("plain")
                        if self.IsJapVerb==1:
                            return [1,13]
                        else:
                            return [22,34]
            elif self.HasTe==1:
                if self.HasMasu==1:
                    if self.HasMasuRYK==0 and self.HasMasuMZN==0:
                        if DEBUG==1:
                            print ("progressive, masu, present")
                        if self.IsJapVerb==1:
                            return [21]
                        else:
                            return [42]
                    elif self.HasMasuMZN==1 and self.HasTa==0:
                        if DEBUG==1:
                            print ("progressive, masu, present, negative")
                        if self.IsJapVerb==1:
                            return [20]
                        else:
                            return [41]
                elif self.HasMasu==0:
                    if self.HasIru==1:
                        if self.HasNai==1 and self.HasTa==0:
                            if DEBUG==1:
                                print ("progressive, plain, present, negative")
                            if self.IsJapVerb==1:
                                return [19]
                            else:
                                return [40]
                        elif self.HasTa==0 and self.HasNai==0:
                            if DEBUG==1:
                                print ("Progressive, plain, present")
                            if self.IsJapVerb==1:
                                return [18]
                            else:
                                return [39]
                    else:
                        if DEBUG==1:
                            print ("te-form")
                        if self.IsJapVerb==1:
                            return [3]
                        else:
                            return [24]
        elif self.IsPotential==1:
            if self.HasTe==0:
                if self.HasTa==0:
                    if DEBUG==1:
                        print ("Potential, present")
                    if self.IsJapVerb==1:
                        return [11]
                    else:
                        return [32]
                elif self.HasTa==1:
                    if DEBUG==1:
                        print ("Potential, past")
                    if self.IsJapVerb==1:
                        return [12]
                    else:
                        return [33]
            else:
                if DEBUG==1:
                    print ("Potential, te-form")
                if self.IsJapVerb==1:
                    return [10]
                else:
                    return [31]
            
        
        