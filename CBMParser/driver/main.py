#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-      

from CBMDriver import CBMDriver
from ParaProc import *
import exrex

def main():
    #verb = input("Enter a verb to be converted to keigo: ")
    #v = VerbAnalyzer_old("使った")
    #v.AnalyzeVerb()
    #print (v.VerbParameters())
    #######################################
    #answer = input("Rewrite the above verb to naru keigo or nasaru keigo: ")
    #x = CBMDriver("お使いになった")
    #x.genPatternBase(v.VerbParameters())
    #x.Verify()
    #x.PrintFeedback()
    #######################################
    #Old scratch codes
    #x = CBMDriver("お使いになる", "使う", 2)
    #x.Verify()
    #x.ShowAnswer()
    #x.PrintFeedback()
    #print (inv_mapping)
    #######################################
    #print (d.targets)
    #print(d.SymToChar(i[2]))

    x = CBMDriver("使わない", "お使いにならない", 1)
    if x.Verify():
        print ("correct")
    else:
        print ("wrong")
        print (x.ShowAnswer())
    #x.ShowAnswer()
    #print(x.PrintFeedback())
    #######################################
    #c = ParagraphPreprocessor("塗り物のおまるをその都度お使いになるのだったが、和宮は今フキがきて二度目の月水の最中で、御用が済むと藤が布を使う。あるかたは売却して資金を得られますから、ごく普通のサラリーマンでも任意後見制度を利用なさるかたはいらっしゃいますよ」と中山さん。")
    #c.MarkExpressions()
    #print (c.MarkedSentences)
    #d.ExprCollect("まるのを見ると、紳士はそれを宥めるようにお使いになった。　「いや、貴君がお怒りになり、お驚きになるのももっともです。が、あゝした人には、近よらないのが万全の策です。あなたが")
    #print(d.IdxToSymbol())
    #print(d.Candidates)
    #for i in d.IdxToSymbol():
    #    test = Tokenizer(i)
    #    test.LexCheck()
    #    print(test.CheckSymbols())
    #test = ConstraintBase()
    #y = Tokenizer("ご利用になるには送金登録を行なう必要があります。")
    #y.SentenceTokenizer()
    #print (y.SentenceSymbols)
    #z = Tokenizer("ご利用になる")
    #z.LexCheck()
    #print (z.ExpressionSymbols)
    #rules = ConstraintBase()
    #print (rules.inv_mapping)
    #print (rules.UnkDict)
    #print (test.inv_mapping)
    #print (test.UnkDict)
    #print (test.ExceptionList[0][0])
    #if '使える' in (x[0] for x in test.ExceptionList):
        #print ("match was found")
    #print (UnkDict)
    #p = test.find_all_paths('K', 'S')
    #test.regexGen(p)
    #for i in test.constraint:
    #    print (i)
    #print(y.VerbSubX('ご利用になる'))
    #pattern_offset, text_offset = z.partial_pattern_match(test.constraint[0])
    #print ("pattern, pattern_offset", test.constraint[0], repr(pattern_offset))
    #print ("good pattern", test.constraint[0][:pattern_offset])
    #print ("text:")
    #print (text)
    #print ('ー' * text_offset + '^')
    #y.TestString()
    #x = Parser("お使いになる")
    #x.parse(3)
    #sample = x.doushiOnly
    #for j in sample[2]:
    #    print (j.Word)
### Execute                                                                                                                                                       
if __name__ == "__main__":
    main()