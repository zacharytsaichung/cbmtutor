#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-  
from Word import Word
import re
import csv

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ConstraintBase(metaclass=Singleton):
    def csv_reader(self, utf8_data, delimiter=',', **kwargs):
        csv_reader = csv.reader(utf8_data, delimiter=delimiter, **kwargs)
        for row in csv_reader:
            yield row
    def __init__(self):
        self.ExceptionList=[]
        exceptions = self.csv_reader(open('exceptions.csv'))
        for i in exceptions:
            self.ExceptionList.append(i)
        #POS to symbol mapping used by the parser.
        self.mapping={Word('お','接頭辞','*','*','*','*','*','お','オ','オ','和'):'A1',
             Word('ご','接頭辞','*','*','*','*','*','ご','ゴ','ゴ','漢'):'A2',
             Word('御','接頭辞','*','*','*','*','*','御','ゴ','ゴ','漢'):'A3',
             Word('御','接頭辞','*','*','*','*','*','御','オ','オ','和'):'A4',
             Word('に', '助詞', '格助詞', '*', '*', '*', '*', 'に', 'ニ', 'ニ','和'):'B1',
             Word('なる','動詞','非自立可能','*','*','五段-ラ行','終止形-一般','なる','ナル','ナル','和'):'C2',
             Word('なる','動詞','非自立可能','*','*','五段-ラ行','連体形-一般','なる','ナル','ナル','和'):'C7',
             Word('なり','動詞','非自立可能','*','*','五段-ラ行','連用形-一般','なる','ナリ','ナル','和'):'C1',
             Word('なれる','動詞','非自立可能','*','*','下一段-ラ行','終止形-一般','なれる','ナレル','ナレル','和'):'C6',
             Word('なれる','動詞','非自立可能','*','*','下一段-ラ行','連体形-一般','なれる','ナレル','ナレル','和'):'C8',
             Word('なら','動詞','非自立可能','*','*','五段-ラ行','未然形-一般','なる','ナラ','ナル','和'):'C4',
             Word('ない','助動詞','*','*','*','助動詞-ナイ','終止形-一般','ない','ナイ','ナイ','和'):'E5',
             Word('ない','助動詞','*','*','*','助動詞-ナイ','連体形-一般','ない','ナイ','ナイ','和'):'E8',
             Word('なっ','動詞','非自立可能','*','*','五段-ラ行','連用形-促音便','なる','ナッ','ナル','和'):'C5',
             Word('なれ','動詞','非自立可能','*','*','下一段-ラ行','連用形-一般','なれる','ナレ','ナレル','和'):'C3',
             Word('て','助詞','接続助詞','*','*','*','*','て','テ','テ','和'):'E6',
             Word('なかっ','助動詞','*','*','*','助動詞-ナイ','連用形-促音便','ない','ナカッ','ナイ','和'):'E7',
             Word('ます','助動詞','*','*','*','助動詞-マス','終止形-一般','ます','マス','マス','和'):'E1',
             Word('た','助動詞','*','*','*','助動詞-タ','終止形-一般','た','タ','タ','和'):'F4',
             Word('た','助動詞','*','*','*','助動詞-タ','連体形-一般','た','タ','タ','和'):'F6',
             Word('まし','助動詞','*','*','*','助動詞-マス','連用形-一般','ます','マシ','マス','和'):'E2',
             Word('ませ','助動詞','*','*','*','助動詞-マス','未然形-一般','ます','マセ','マス','和'):'E3',
             Word('ん','助動詞','*','*','*','助動詞-ヌ','終止形-撥音便','ぬ','ン','ヌ','和'):'F1',
             Word('いる','動詞','非自立可能','*','*','上一段-ア行','終止形-一般','いる','イル','イル','和'):'F3',
             Word('いる','動詞','非自立可能','*','*','上一段-ア行','連体形-一般','いる','イル','イル','和'):'F7',
             Word('い','動詞','非自立可能','*','*','上一段-ア行','連用形-一般','いる','イ','イル','和'):'F2',
             Word('い','動詞','非自立可能','*','*','上一段-ア行','未然形-一般','いる','イ','イル','和'):'F5',
             Word('でし','助動詞','*','*','*','助動詞-デス','連用形-一般','です','デシ','デス','和'):'G1',
             Word('れる','助動詞','*','*','*','助動詞-レル','終止形-一般','れる','レル','レル','和'):'D2',
             Word('れ','助動詞','*','*','*','助動詞-レル','連用形-一般','れる','レ','レル','和'):'D1',
             Word('れ','助動詞','*','*','*','助動詞-レル','未然形-一般','れる','レ','レル','和'):'D3',
             Word('なさり','動詞','非自立可能','*','*','五段-ラ行','連用形-一般','なさる','ナサリ','ナサル','和'):'B8',
             Word('なさる','動詞','非自立可能','*','*','五段-ラ行','終止形-一般','なさる','ナサル','ナサル','和'):'B9',
             Word('なさる','動詞','非自立可能','*','*','五段-ラ行','連体形-一般','なさる','ナサル','ナサル','和'):'B22',
             Word('なさら','動詞','非自立可能','*','*','五段-ラ行','未然形-一般','なさる','ナサラ','ナサル','和'):'B10',
             Word('なさっ','動詞','非自立可能','*','*','五段-ラ行','連用形-促音便','なさる','ナサッ','ナサル','和'):'B11',
             #Word('なさ','動詞','一般','*','*','五段-サ行','未然形-一般','なす','ナサ','ナス','和'):'B12',
             Word('なされる','動詞','非自立可能','*','*','下一段-ラ行','終止形-一般','なされる','ナサレル','ナサレル','和'):'B13',
             Word('する','動詞','非自立可能','*','*','サ行変格','終止形-一般','する','スル','スル','和'):'B14',
             Word('する','動詞','非自立可能','*','*','サ行変格','連体形-一般','する','スル','スル','和'):'B23',
             Word('し','動詞','非自立可能','*','*','サ行変格','連用形-一般','する','シ','スル','和'):'B15',
             Word('できる','動詞','非自立可能','*','*','上一段-カ行','終止形-一般','できる','デキル','デキル','和'):'B16',
             Word('でき','動詞','非自立可能','*','*','上一段-カ行','連用形-一般','できる','デキ','デキル','和'):'B17',
             Word('し','動詞','非自立可能','*','*','サ行変格','未然形-一般','する','シ','スル','和'):'B18',
             Word('でき','動詞','非自立可能','*','*','上一段-カ行','未然形-一般','できる','デキ','デキル','和'):'B19',
             Word('られる','助動詞','*','*','*','助動詞-レル','終止形-一般','られる','ラレル','ラレル','和'):'B20',
             Word('られ','助動詞','*','*','*','助動詞-レル','連用形-一般','られる','ラレ','ラレル','和'):'B21'
             }
    
        #Symbol to　character mapping.
        self.inv_mapping = {v: k for k, v in self.mapping.items()}
    
        #Patterns acceptable to the CBM Parser. This is the Satisfaction condition, assuming the goal is rewriting from regular to honorific polite.
        #Note: In parsing (runtime), we add W as a BOS and Y as EOS marker.
        
        #As of 10/22, no negatives of potential forms are included yet and double keigo of nasaru
        self.rbase={'X4':['(A4|A1)X1B1(C2|C7)','(A4|A1){0,1}X1(B9|B22)','(A4|A1)X1B1C4D2'],# for taberu -> keigo
               'X3':['(A4|A1)X9B1(C2|C7)','(A4|A1){0,1}X9(B9|B22)','(A4|A1)X9B1C4D2'],# for tsukau -> keigo
               'X5(F4|F6)':['(A4|A1)X1B1C5(F4|F6)','(A4|A1){0,1}X1B11(F4|F6)','(A4|A1)X1B1C4D1(F4|F6)'], #for tsukatta ->keigo
               'X9(F4|F6)':['(A4|A1)X9B1C5(F4|F6)','(A4|A1){0,1}X9B11(F4|F6)','(A4|A1)X9B1C4D1(F4|F6)'], #for tabeta ->keigo
               'X5E6':['(A4|A1)X1B1C5E6','(A4|A1){0,1}X1B11E6','(A4|A1)X1B1C4D1E6'], #for tsukatte ->keigo
               'X9E6':['(A4|A1)X9B1C5E6','(A4|A1){0,1}X9B11E6','(A4|A1)X9B1C4D1E6'], #for tsukatte ->keigo
               'X1E1':['(A4|A1)X1B1C1E1','(A4|A1){0,1}X1B8E1','(A4|A1)X1B1C4D1E1'], #for tsukaimasu ->keigo
               'X9E1':['(A4|A1)X9B1C1E1','(A4|A1){0,1}X9B8E1','(A4|A1)X9B1C4D1E1'], #for tabemasu ->keigo
               'X1E2(F4|F6)':['(A4|A1)X1B1C1E2(F4|F6)','(A4|A1){0,1}X1B8E2(F4|F6)','(A4|A1)X1B1C4D1E2(F4|F6)'], #for tsukaimashita ->keigo
               'X9E2(F4|F6)':['(A4|A1)X9B1C1E2(F4|F6)','(A4|A1){0,1}X9B8E2(F4|F6)','(A4|A1)X9B1C4D1E2(F4|F6)'], #for tabemashita ->keigo
               'X1E3F1':['(A4|A1)X1B1C1E3F1','(A4|A1){0,1}X1B8E3F1','(A4|A1)X1B1C4D1E3F1'], #for tsukaimasen ->keigo
               'X9E3F1':['(A4|A1)X9B1C1E3F1','(A4|A1){0,1}X9B8E3F1','(A4|A1)X9B1C4D1E3F1'], #for tabemasen ->keigo
               'X1E3F1G1(F4|F6)':['(A4|A1)X1B1C1E3F1G1(F4|F6)','(A4|A1){0,1}X1B8E3F1G1(F4|F6)','(A4|A1)X1B1C4D1E3F1G1(F4|F6)'], #tsukaimasendeshita->keigo
               'X9E3F1G1(F4|F6)':['(A4|A1)X9B1C1E3F1G1(F4|F6)','(A4|A1){0,1}X9B8E3F1G1(F4|F6)','(A4|A1)X9B1C4D1E3F1G1(F4|F6)'], #tabemasendeshita->keigo
               'X6(E5|E8)':['(A4|A1)X1B1C4(E5|E8)','(A4|A1){0,1}X1B10(E5|E8)','(A4|A1)X1B1C4D1(E5|E8)'], #tsukawanai->keigo
               'X10(E5|E8)':['(A4|A1)X9B1C4(E5|E8)','(A4|A1){0,1}X9B10(E5|E8)','(A4|A1)X9B1C4D1(E5|E8)'], #tabenai->keigo
               'X6E7(F4|F6)':['(A4|A1)X1B1C4E7(F4|F6)','(A4|A1){0,1}X1B10E7(F4|F6)','(A4|A1)X1B1C4D1E7(F4|F6)'],
               'X10E7(F4|F6)':['(A4|A1)X9B1C4E7(F4|F6)','(A4|A1){0,1}X9B10E7(F4|F6)','(A4|A1)X9B1C4D1E7(F4|F6)'],
               'X8E6':['(A4|A1)X1B1C3E6'], #tsukaete ->keigo
               'X10B21E6':['(A4|A1)X9B1C3E6'], #taberarete ->keigo
               'X7':['(A4|A1)X1B1(C6|C8)'], #tsukaeru->keigo
               'X10B20':['(A4|A1)X9B1(C6|C8)'],#taberareru->keigo
               'X8(F4|F6)':['(A4|A1)X1B1C3(F4|F6)'], #tsukaeta->keigo
               'X10B21(F4|F6)':['(A4|A1)X9B1C3(F4|F6)'],#taberareta->keigo
               'X5E6(F3|F7)':['(A4|A1)X1B1C5E6(F3|F7)','(A4|A1){0,1}X1B11E6(F3|F7)'], #teiru
               'X9E6(F3|F7)':['(A4|A1)X9B1C5E6(F3|F7)','(A4|A1){0,1}X9B11E6(F3|F7)'], #teiru
               'X5E6F5(E5|E8)':['(A4|A1)X1B1C5E6F5(E5|E8)','(A4|A1){0,1}X1B11E6F5(E5|E8)'], #teinai
               'X9E6F5(E5|E8)':['(A4|A1)X9B1C5E6F5(E5|E8)','(A4|A1){0,1}X9B11E6F5(E5|E8)'], #teinai
               'X5E6F2E3F1':['(A4|A1)X1B1C5E6F2E3F1','(A4|A1){0,1}X1B11E6F2E3F1'], #teimasen
               'X9E6F2E3F1':['(A4|A1)X9B1C5E6F2E3F1','(A4|A1){0,1}X9B11E6F2E3F1'], #teimasen
               'X5E6F2E1':['(A4|A1)X1B1C5E6F2E1','(A4|A1){0,1}X1B11E6F2E1'], #teimasu
               'X9E6F2E1':['(A4|A1)X9B1C5E6F2E1','(A4|A1){0,1}X9B11E6F2E1'], #teimasu
               #Go prefixed expressions
               'X2(B14|B23)':['(A3|A2)X2B1(C2|C7)','(A3|A2){0,1}X2(B9|B22)','(A3|A2)X2B1C4D2'],
               'X2B15(F4|F6)':['(A3|A2)X2B1C5(F4|F6)','(A3|A2){0,1}X2B11(F4|F6)','(A3|A2)X2B1C4D1(F4|F6)'],
               'X2B15E6':['(A3|A2)X2B1C5E6','(A3|A2){0,1}X2B11E6','(A3|A2)X2B1C4D1E6'],
               'X2B15E1':['(A3|A2)X2B1C1E1','(A3|A2){0,1}X2B8E1','(A3|A2)X2B1C4D1E1'],
               'X2B15E2(F4|F6)':['(A3|A2)X2B1C1E2(F4|F6)','(A3|A2){0,1}X2B8E2(F4|F6)','(A3|A2)X2B1C4D1E2(F4|F6)'],
               'X2B15E3F1':['(A3|A2)X2B1C1E3F1','(A3|A2){0,1}X2B8E3F1','(A3|A2)X2B1C4D1E3F1'],
               'X2B15E3F1G1(F4|F6)':['(A3|A2)X2B1C1E3F1G1(F4|F6)','(A3|A2){0,1}X2B8E3F1G1(F4|F6)','(A3|A2)X2B1C4D1E3F1G1(F4|F6)'],
               'X2B18(E5|E8)':['(A3|A2)X2B1C4(E5|E8)','(A3|A2){0,1}X2B10(E5|E8)','(A3|A2)X2B1C4D1(E5|E8)'],
               'X2B18E7(F4|F6)':['(A3|A2)X2B1C4E7(F4|F6)','(A3|A2){0,1}X2B10E7(F4|F6)','(A3|A2)X2B1C4D1E7(F4|F6)'],
               'X2B17E6':['(A3|A2)X2B1C3E6'],
               'X2B16':['(A3|A2)X2B1(C6|C8)'],
               'X2B17(F4|F6)':['(A3|A2)X2B1C3(F4|F6)'],
               'X2B15E6(F3|F7)':['(A3|A2)X2B1C5E6(F3|F7)','(A3|A2){0,1}X2B11E6(F3|F7)'],
               'X2B15E6F5(E5|E8)':['(A3|A2)X2B1C5E6F5(E5|E8)','(A3|A2){0,1}X2B11E6F5(E5|E8)'],
               'X2B15E6F2E3F1':['(A3|A2)X2B1C5E6F2E3F1','(A3|A2){0,1}X2B11E6F2E3F1'],
               'X2B15E6F2E1':['(A3|A2)X2B1C5E6F2E1','(A3|A2){0,1}X2B11E6F2E1']
               }
        #Reverse of the rules above. The Satisfaction condition becomes the relevance condition, assuming the prupose is from honorific polite to regular.
        #Again, X is a BOS marker and Y is an EOS marker.
        #As of Oct 13, 2016, the BOS/EOS marker has been removed.
        self.inv_rules = {v: k for k in self.rbase for v in self.rbase[k]}
        
        self.rules = {k: v for k, v in self.rbase.items()}
        
        #Controls the maximum number of results to get from MeCab.
        self.NBEST = 3
        
        #Dictionary store of unknown POS and its corresponding symbol assignment.
        self.UnkDict = {}
        
        self.inv_UnkDict = {}
        
"""
#Controls the maximum number of results to get from MeCab.
NBEST = 3

#Dictionary store of unknown POS and its corresponding symbol assignment.
UnkDict = {}

inv_UnkDict = {v: k for k, v in UnkDict.items()}

#A custom dict which can reject with ValueError if the key is already present.
#See: http://stackoverflow.com/questions/4999233/how-to-raise-error-if-duplicates-keys-in-dictionary
class RejectingDict(dict):
    def __setitem__(self, k, v):
        if k in self.keys():
            raise ValueError("Key is already present")
        else:
            return super(RejectingDict, self).__setitem__(k, v)

#POS to symbol mapping used by the parser.
mapping={Word('お','接頭辞','*','*','*','*','*','お','オ','オ','和'):'A1',
         Word('ご','接頭辞','*','*','*','*','*','ご','ゴ','ゴ','漢'):'A2',
         Word('御','接頭辞','*','*','*','*','*','御','ゴ','ゴ','漢'):'A3',
         Word('御','接頭辞','*','*','*','*','*','御','オ','オ','和'):'A4',
         Word('に', '助詞', '格助詞', '*', '*', '*', '*', 'に', 'ニ', 'ニ','和'):'B1',
         Word('なる','動詞','非自立可能','*','*','五段-ラ行','終止形-一般','なる','ナル','ナル','和'):'C2',
         Word('なる','動詞','非自立可能','*','*','五段-ラ行','連体形-一般','なる','ナル','ナル','和'):'C7',
         Word('なり','動詞','非自立可能','*','*','五段-ラ行','連用形-一般','なる','ナリ','ナル','和'):'C1',
         Word('なれる','動詞','非自立可能','*','*','下一段-ラ行','終止形-一般','なれる','ナレル','ナレル','和'):'C6',
         Word('なれる','動詞','非自立可能','*','*','下一段-ラ行','連体形-一般','なれる','ナレル','ナレル','和'):'C8',
         Word('なら','動詞','非自立可能','*','*','五段-ラ行','未然形-一般','なる','ナラ','ナル','和'):'C4',
         Word('ない','助動詞','*','*','*','助動詞-ナイ','終止形-一般','ない','ナイ','ナイ','和'):'E5',
         Word('ない','助動詞','*','*','*','助動詞-ナイ','連体形-一般','ない','ナイ','ナイ','和'):'E8',
         Word('なっ','動詞','非自立可能','*','*','五段-ラ行','連用形-促音便','なる','ナッ','ナル','和'):'C5',
         Word('なれ','動詞','非自立可能','*','*','下一段-ラ行','連用形-一般','なれる','ナレ','ナレル','和'):'C3',
         Word('て','助詞','接続助詞','*','*','*','*','て','テ','テ','和'):'E6',
         Word('なかっ','助動詞','*','*','*','助動詞-ナイ','連用形-促音便','ない','ナカッ','ナイ','和'):'E7',
         Word('ます','助動詞','*','*','*','助動詞-マス','終止形-一般','ます','マス','マス','和'):'E1',
         Word('た','助動詞','*','*','*','助動詞-タ','終止形-一般','た','タ','タ','和'):'F4',
         Word('た','助動詞','*','*','*','助動詞-タ','連体形-一般','た','タ','タ','和'):'F6',
         Word('まし','助動詞','*','*','*','助動詞-マス','連用形-一般','ます','マシ','マス','和'):'E2',
         Word('ませ','助動詞','*','*','*','助動詞-マス','未然形-一般','ます','マセ','マス','和'):'E3',
         Word('ん','助動詞','*','*','*','助動詞-ヌ','終止形-撥音便','ぬ','ン','ヌ','和'):'F1',
         Word('いる','動詞','非自立可能','*','*','上一段-ア行','終止形-一般','いる','イル','イル','和'):'F3',
         Word('いる','動詞','非自立可能','*','*','上一段-ア行','連体形-一般','いる','イル','イル','和'):'F7',
         Word('い','動詞','非自立可能','*','*','上一段-ア行','連用形-一般','いる','イ','イル','和'):'F2',
         Word('い','動詞','非自立可能','*','*','上一段-ア行','未然形-一般','いる','イ','イル','和'):'F5',
         Word('でし','助動詞','*','*','*','助動詞-デス','連用形-一般','です','デシ','デス','和'):'G1',
         Word('れる','助動詞','*','*','*','助動詞-レル','終止形-一般','れる','レル','レル','和'):'D2',
         Word('れ','助動詞','*','*','*','助動詞-レル','連用形-一般','れる','レ','レル','和'):'D1',
         Word('れ','助動詞','*','*','*','助動詞-レル','未然形-一般','れる','レ','レル','和'):'D3',
         Word('なさり','動詞','非自立可能','*','*','五段-ラ行','連用形-一般','なさる','ナサリ','ナサル','和'):'B8',
         Word('なさる','動詞','非自立可能','*','*','五段-ラ行','終止形-一般','なさる','ナサル','ナサル','和'):'B9',
         Word('なさる','動詞','非自立可能','*','*','五段-ラ行','連体形-一般','なさる','ナサル','ナサル','和'):'B22',
         Word('なさら','動詞','非自立可能','*','*','五段-ラ行','未然形-一般','なさる','ナサラ','ナサル','和'):'B10',
         Word('なさっ','動詞','非自立可能','*','*','五段-ラ行','連用形-促音便','なさる','ナサッ','ナサル','和'):'B11',
         #Word('なさ','動詞','一般','*','*','五段-サ行','未然形-一般','なす','ナサ','ナス','和'):'B12',
         Word('なされる','動詞','非自立可能','*','*','下一段-ラ行','終止形-一般','なされる','ナサレル','ナサレル','和'):'B13',
         Word('する','動詞','非自立可能','*','*','サ行変格','終止形-一般','する','スル','スル','和'):'B14',
         Word('する','動詞','非自立可能','*','*','サ行変格','連体形-一般','する','スル','スル','和'):'B23',
         Word('し','動詞','非自立可能','*','*','サ行変格','連用形-一般','する','シ','スル','和'):'B15',
         Word('できる','動詞','非自立可能','*','*','上一段-カ行','終止形-一般','できる','デキル','デキル','和'):'B16',
         Word('でき','動詞','非自立可能','*','*','上一段-カ行','連用形-一般','できる','デキ','デキル','和'):'B17',
         Word('し','動詞','非自立可能','*','*','サ行変格','未然形-一般','する','シ','スル','和'):'B18',
         Word('でき','動詞','非自立可能','*','*','上一段-カ行','未然形-一般','できる','デキ','デキル','和'):'B19',
         Word('られる','助動詞','*','*','*','助動詞-レル','終止形-一般','られる','ラレル','ラレル','和'):'B20',
         Word('られ','助動詞','*','*','*','助動詞-レル','連用形-一般','られる','ラレ','ラレル','和'):'B21'
         }

#Symbol to　character mapping.
inv_mapping = {v: k for k, v in mapping.items()}

#Patterns acceptable to the CBM Parser. This is the Satisfaction condition, assuming the goal is rewriting from regular to honorific polite.
#Note: In parsing (runtime), we add W as a BOS and Y as EOS marker.

#As of 10/22, no negatives of potential forms are included yet and double keigo of nasaru
rules={'X4':['(A4|A1)X1B1(C2|C7)','(A4|A1)*X1(B9|B22)','(A4|A1)X1B1C4D2'],# for taberu -> keigo
       'X3':['(A4|A1)X9B1(C2|C7)','(A4|A1)*X9(B9|B22)','(A4|A1)X9B1C4D2'],# for tsukau -> keigo
       'X5(F4|F6)':['(A4|A1)X1B1C5(F4|F6)','(A4|A1)*X1B11(F4|F6)','(A4|A1)X1B1C4D1(F4|F6)'], #for tsukatta ->keigo
       'X9(F4|F6)':['(A4|A1)X9B1C5(F4|F6)','(A4|A1)*X9B11(F4|F6)','(A4|A1)X9B1C4D1(F4|F6)'], #for tabeta ->keigo
       'X5E6':['(A4|A1)X1B1C5E6','(A4|A1)*X1B11E6','(A4|A1)X1B1C4D1E6'], #for tsukatte ->keigo
       'X9E6':['(A4|A1)X9B1C5E6','(A4|A1)*X9B11E6','(A4|A1)X9B1C4D1E6'], #for tsukatte ->keigo
       'X1E1':['(A4|A1)X1B1C1E1','(A4|A1)*X1B8E1','(A4|A1)X1B1C4D1E1'], #for tsukaimasu ->keigo
       'X9E1':['(A4|A1)X9B1C1E1','(A4|A1)*X9B8E1','(A4|A1)X9B1C4D1E1'], #for tabemasu ->keigo
       'X1E2(F4|F6)':['(A4|A1)X1B1C1E2(F4|F6)','(A4|A1)*X1B8E2(F4|F6)','(A4|A1)X1B1C4D1E2(F4|F6)'], #for tsukaimashita ->keigo
       'X9E2(F4|F6)':['(A4|A1)X9B1C1E2(F4|F6)','(A4|A1)*X9B8E2(F4|F6)','(A4|A1)X9B1C4D1E2(F4|F6)'], #for tabemashita ->keigo
       'X1E3F1':['(A4|A1)X1B1C1E3F1','(A4|A1)*X1B8E3F1','(A4|A1)X1B1C4D1E3F1'], #for tsukaimasen ->keigo
       'X9E3F1':['(A4|A1)X9B1C1E3F1','(A4|A1)*X9B8E3F1','(A4|A1)X9B1C4D1E3F1'], #for tabemasen ->keigo
       'X1E3F1G1(F4|F6)':['(A4|A1)X1B1C1E3F1G1(F4|F6)','(A4|A1)*X1B8E3F1G1(F4|F6)','(A4|A1)X1B1C4D1E3F1G1(F4|F6)'], #tsukaimasendeshita->keigo
       'X9E3F1G1(F4|F6)':['(A4|A1)X9B1C1E3F1G1(F4|F6)','(A4|A1)*X9B8E3F1G1(F4|F6)','(A4|A1)X9B1C4D1E3F1G1(F4|F6)'], #tabemasendeshita->keigo
       'X6(E5|E8)':['(A4|A1)X1B1C4(E5|E8)','(A4|A1)*X1B10(E5|E8)','(A4|A1)X1B1C4D1(E5|E8)'], #tsukawanai->keigo
       'X10(E5|E8)':['(A4|A1)X9B1C4(E5|E8)','(A4|A1)*X9B10(E5|E8)','(A4|A1)X9B1C4D1(E5|E8)'], #tabenai->keigo
       'X6E7(F4|F6)':['(A4|A1)X1B1C4E7(F4|F6)','(A4|A1)*X1B10E7(F4|F6)','(A4|A1)X1B1C4D1E7(F4|F6)'],
       'X10E7(F4|F6)':['(A4|A1)X9B1C4E7(F4|F6)','(A4|A1)*X9B10E7(F4|F6)','(A4|A1)X9B1C4D1E7(F4|F6)'],
       'X8E6':['(A4|A1)X1B1C3E6'], #tsukaete ->keigo
       'X10B21E6':['(A4|A1)X9B1C3E6'], #taberarete ->keigo
       'X7':['(A4|A1)X1B1(C6|C8)'], #tsukaeru->keigo
       'X10B20':['(A4|A1)X9B1(C6|C8)'],#taberareru->keigo
       'X8(F4|F6)':['(A4|A1)X1B1C3(F4|F6)'], #tsukaeta->keigo
       'X10B21(F4|F6)':['(A4|A1)X9B1C3(F4|F6)'],#taberareta->keigo
       'X5E6(F3|F7)':['(A4|A1)X1B1C5E6(F3|F7)','(A4|A1)*X1B11E6(F3|F7)'], #teiru
       'X9E6(F3|F7)':['(A4|A1)X9B1C5E6(F3|F7)','(A4|A1)*X9B11E6(F3|F7)'], #teiru
       'X5E6F5(E5|E8)':['(A4|A1)X1B1C5E6F5(E5|E8)','(A4|A1)*X1B11E6F5(E5|E8)'], #teinai
       'X9E6F5(E5|E8)':['(A4|A1)X9B1C5E6F5(E5|E8)','(A4|A1)*X9B11E6F5(E5|E8)'], #teinai
       'X5E6F2E3F1':['(A4|A1)X1B1C5E6F2E3F1','(A4|A1)*X1B11E6F2E3F1'], #teimasen
       'X9E6F2E3F1':['(A4|A1)X9B1C5E6F2E3F1','(A4|A1)*X9B11E6F2E3F1'], #teimasen
       'X5E6F2E1':['(A4|A1)X1B1C5E6F2E1','(A4|A1)*X1B11E6F2E1'], #teimasu
       'X9E6F2E1':['(A4|A1)X9B1C5E6F2E1','(A4|A1)*X9B11E6F2E1'], #teimasu
       #Go prefixed expressions
       'X2(B14|B23)':['(A3|A2)X2B1(C2|C7)','(A3|A2)*X2(B9|B22)','(A3|A2)X2B1C4D2'],
       'X2B15(F4|F6)':['(A3|A2)X2B1C5(F4|F6)','(A3|A2)*X2B11(F4|F6)','(A3|A2)X2B1C4D1(F4|F6)'],
       'X2B15E6':['(A3|A2)X2B1C5E6','(A3|A2)*X2B11E6','(A3|A2)X2B1C4D1E6'],
       'X2B15E1':['(A3|A2)X2B1C1E1','(A3|A2)*X2B8E1','(A3|A2)X2B1C4D1E1'],
       'X2B15E2(F4|F6)':['(A3|A2)X2B1C1E2(F4|F6)','(A3|A2)*X2B8E2(F4|F6)','(A3|A2)X2B1C4D1E2(F4|F6)'],
       'X2B15E3F1':['(A3|A2)X2B1C1E3F1','(A3|A2)*X2B8E3F1','(A3|A2)X2B1C4D1E3F1'],
       'X2B15E3F1G1(F4|F6)':['(A3|A2)X2B1C1E3F1G1(F4|F6)','(A3|A2)*X2B8E3F1G1(F4|F6)','(A3|A2)X2B1C4D1E3F1G1(F4|F6)'],
       'X2B18(E5|E8)':['(A3|A2)X2B1C4(E5|E8)','(A3|A2)*X2B10(E5|E8)','(A3|A2)X2B1C4D1(E5|E8)'],
       'X2B18E7(F4|F6)':['(A3|A2)X2B1C4E7(F4|F6)','(A3|A2)*X2B10E7(F4|F6)','(A3|A2)X2B1C4D1E7(F4|F6)'],
       'X2B17E6':['(A3|A2)X2B1C3E6'],
       'X2B16':['(A3|A2)X2B1(C6|C8)'],
       'X2B17(F4|F6)':['(A3|A2)X2B1C3(F4|F6)'],
       'X2B15E6(F3|F7)':['(A3|A2)X2B1C5E6(F3|F7)','(A3|A2)*X2B11E6(F3|F7)'],
       'X2B15E6F5(E5|E8)':['(A3|A2)X2B1C5E6F5(E5|E8)','(A3|A2)*X2B11E6F5(E5|E8)'],
       'X2B15E6F2E3F1':['(A3|A2)X2B1C5E6F2E3F1','(A3|A2)*X2B11E6F2E3F1'],
       'X2B15E6F2E1':['(A3|A2)X2B1C5E6F2E1','(A3|A2)*X2B11E6F2E1']
       }

#Reverse of the rules above. The Satisfaction condition becomes the relevance condition, assuming the prupose is from honorific polite to regular.
#Again, X is a BOS marker and Y is an EOS marker.
#As of Oct 13, 2016, the BOS/EOS marker has been removed.
inv_rules = {re.compile(v): k for k in rules for v in rules[k]}
"""