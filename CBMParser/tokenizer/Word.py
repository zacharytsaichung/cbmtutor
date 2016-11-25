#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-                                                                                                                                            

"""Word Class: Contains the result of a POS analysis from MeCab; can be used as a dictionary key"""
"""Parameter:
    word - the POS itself.
    pos - 品詞
    spos1 - 品詞細分類1
    spos2 - 品詞細分類2
    spos3 - 品詞細分類3
    goDan - 活用形
    conjugation - 活用型
    dictForm - 原形
    reading - 読み
    pronunciation - 発音
    WaKan - NEW - identifies if the verb is kango or wago (optional). This is only available in Unidic!
"""
    
class Word:
    def __init__(self, word='',pos='',spos1='',spos2='',spos3='', goDan='', conjugation='', dictForm='', reading='', pronunciation='', WaKan=''): 
        self.word = word
        self.pos = pos
        self.spos1 = spos1
        self.spos2 = spos2
        self.spos3 = spos3
        self.reading = reading
        self.goDan = goDan
        self.dictForm = dictForm
        self.conjugation = conjugation
        self.pronunciation = pronunciation
        self.WaKan = WaKan
    def __hash__(self):
        HashValue = hash((self.word, self.pos, self.spos1, self.spos2, self.spos3, self.goDan, self.conjugation, 
                          self.dictForm, self.reading, self.pronunciation, self.WaKan)) 
        return HashValue
    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        if other.word==self.word and other.pos==self.pos and other.spos1==self.spos1 and other.spos2==self.spos2 and \
        other.spos3==self.spos3 and other.reading==self.reading and other.goDan==self.goDan and other.dictForm==self.dictForm and \
        other.conjugation==self.conjugation and other.pronunciation==self.pronunciation and other.WaKan==self.WaKan:
            return self.__class__
    @property
    def word(self):
        return self.__word
    @property
    def pos(self):
        return self.__pos
    @property
    def spos1(self):
        return self.__spos1
    @property
    def spos2(self):
        return self.__spos2
    @property
    def spos3(self):
        return self.__spos3
    @property
    def reading(self):
        return self.__reading
    @property
    def goDan(self):
        return self.__goDan
    @property
    def dictForm(self):
        return self.__dictForm
    @property
    def conjugation(self):
        return self.__conjugation
    @property
    def pronunciation(self):
        return self.__pronunciation
    @property
    def WaKan(self):
        return self.__WaKan
    def getWordAsTuple(self):
        return (self.word, self.pos, self.spos1, self.spos2, self.spos3, self.goDan, self.conjugation, self.dictForm, self.reading, self.pronunciation, self.WaKan)
    @goDan.setter
    def goDan(self, goDan):
        self.__goDan = goDan
    @word.setter
    def word(self, word):
        self.__word = word
    @pos.setter
    def pos(self, pos):
        self.__pos = pos
    @spos1.setter
    def spos1(self, spos1):
        self.__spos1 = spos1
    @spos2.setter
    def spos2(self, spos2):
        self.__spos2 = spos2
    @spos3.setter
    def spos3(self, spos3):
        self.__spos3 = spos3
    @reading.setter
    def reading(self, reading):
        self.__reading = reading
    @dictForm.setter
    def dictForm(self, dictForm):
        self.__dictForm = dictForm
    @conjugation.setter
    def conjugation(self, conjugation):
        self.__conjugation = conjugation
    @pronunciation.setter
    def pronunciation(self, pronunciation):
        self.__pronunciation = pronunciation
    @WaKan.setter
    def WaKan(self, WaKan):
        self.__WaKan = WaKan