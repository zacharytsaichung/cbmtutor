#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-    
import re

#Refer: http://code.activestate.com/recipes/475187-regular-expression-point-of-failure/

def sub_re(pattern):
    for offset in range(len(pattern)+1,0,-1):
        try:
            re_obj = re.compile(pattern[:offset])
        except re.error: # syntax error in re part
            continue
        yield offset, re_obj

def partial_pattern_match(pattern, text):
    good_pattern_offset = 0
    good_text_offset = 0
    for re_offset, re_obj in sub_re(pattern):
        match = re_obj.match(text)
        if match:
            good_pattern_offset = re_offset
            good_text_offset = match.end()
            return good_pattern_offset, good_text_offset
    return good_pattern_offset, good_text_offset

if __name__ == "__main__":
    pattern = r"お使いになりませんでした"
    text = "お使いになりせん"
    pattern_offset, text_offset = partial_pattern_match(pattern, text)
    print ("pattern, pattern_offset", pattern, repr(pattern_offset))
    print ("good pattern", pattern[:pattern_offset])
    print ("text:")
    print (text)
    print (' ' * text_offset + '^')

    pattern = r"a+[bc]+z*e+f"
    text = "aaaaabbbbyef"
    pattern_offset, text_offset = partial_pattern_match(pattern, text)
    print ("pattern, pattern_offset", pattern, repr(pattern_offset))
    print ("good pattern", pattern[:pattern_offset])
    print ("text:")
    print (text)
    print (' ' * text_offset + '^')