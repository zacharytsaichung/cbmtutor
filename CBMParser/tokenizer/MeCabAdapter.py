#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-                                                                                                                                            

import MeCab
from Word import Word

DEBUG=0

### Constants                                                                                                                                                     
MECAB_MODE = 'mecabrc'#MeCabの出力形式パラメータ
DICTIONARY = 'unidic'
"""Description: Parser class to work as an interface to MeCab for getting and manipulating results."""

### Classes
class Parser:
    """self.store contains the n number of MeCab parse results"""
    def __init__(self, unicode_str):
        self.unicode_str = unicode_str
        self.store = []
    """Return n-top results from MeCab. Default 1"""
    def parse(self, nbest=1):
        del self.store[:] #Ensure a clean list to store results before run.
        tagger = MeCab.Tagger(MECAB_MODE)
        tagger.parse('')
        node = tagger.parseNBestInit(self.unicode_str)
        for i in range (nbest):
            results=[]
            node = tagger.nextNode();
            while node:
                if node.feature.split(",")[0] != "BOS/EOS":
                    p = node.feature.split(",")
                    p.insert(0,node.surface)
                    if DICTIONARY=='unidic':
                        if DEBUG==1:
                            print (p)
                        results.append(Word(p[0],p[1],p[2],p[3],p[4],p[5],p[6],p[11],p[10],p[12],p[13]))
                    if DICTIONARY=='ipadic':
                        if DEBUG==1:
                            print (p)
                        results.append(Word(*p))
                node = node.next
            self.store.append(results)
    """doushiOnly - Filter MeCab results such that only 動詞 are returned"""
    @property
    def doushiOnly(self):
        updatedStore = []
        for nresult in self.store:
            results=[]
            for i in nresult:
                if DICTIONARY=='ipadic':
                    if i.pos=="動詞" or i.pos=="名詞" and i.spos1=="サ変接続":
                        results.append(i)
                if DICTIONARY=='unidic':
                    if i.pos=="動詞" and i.spos1=='一般' or i.pos=="名詞" and i.spos2=='サ変可能':
                        results.append(i)
            updatedStore.append(results)
        return updatedStore
    """doushiAll - Filter MeCab results to return both 動詞 and 助動詞 results"""
    @property
    def doushiAll(self):
        updatedStore = []
        for nresult in self.store:
            results=[]
            for i in nresult:
                if DICTIONARY=='ipadic':
                    if i.pos=="動詞" or "助動詞" or (i.pos=="名詞" and i.spos1=="サ変接続"):
                        results.append(i)
                if DICTIONARY=='unidic':
                    if i.pos=="動詞" or "助動詞" or (i.pos=="名詞" and i.spos2=='サ変可能'):
                        results.append(i)
            updatedStore.append(results)
        return updatedStore
    """jodoushi - Filter MeCab results such that only 助動詞 are returned"""
    @property
    def jodoushi(self):
        updatedStore = []
        for nresult in self.store:
            results=[]
            for i in nresult:
                if DICTIONARY=='ipadic':
                    if i.pos=="助動詞":
                        results.append(i)
                if DICTIONARY=='unidic':
                    if i.pos=="助動詞":
                        results.append(i)
            updatedStore.append(results)
        return updatedStore
    """setsubi - Filter MeCab results such that only 接尾 are returned"""
    @property
    def setsubi(self):
        updatedStore = []
        for nresult in self.store:
            results=[]
            for i in nresult:
                if DICTIONARY=='ipadic':
                    if i.pos=="動詞" and i.spos==u"接尾":
                        results.append(i)
                if DICTIONARY=='unidic':
                    if "助動詞" in i.goDan:
                        results.append(i)
            updatedStore.append(results)
        return updatedStore
    """all - Returns all results from MeCab, regardless of POS type"""
    @property
    def all(self):
        return self.store
