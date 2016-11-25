#!/usr/bin/env python                                                                                                                                             
# -*- coding:utf-8 -*-                                                                                                                                            

import re

def utoe(unicode_string):
    if re.search(r'う$', unicode_string):
        return re.sub(r'う$', u'え', unicode_string)
    if re.search(r'く$', unicode_string):
        return re.sub(r'く$', u'け', unicode_string)
    if re.search(r'す$', unicode_string):
        return re.sub(r'す$', u'せ', unicode_string)
    if re.search(r'つ$', unicode_string):
        return re.sub(r'つ$', u'て', unicode_string)
    if re.search(r'ぶ$', unicode_string):
        return re.sub(r'ぶ$', u'べ', unicode_string)
    if re.search(r'ぬ$', unicode_string):
        return re.sub(r'ぬ$', u'ね', unicode_string)
    if re.search(r'る$', unicode_string):
        return re.sub(r'る$', u'れ', unicode_string)
    if re.search(r'む$', unicode_string):
        return re.sub(r'む$', u'め', unicode_string)
    if re.search(r'ぐ$', unicode_string):
        return re.sub(r'ぐ$', u'げ', unicode_string)

def utoer(unicode_string):
    if re.search(r'う$', unicode_string):
        return re.sub(r'う$', u'える', unicode_string)
    if re.search(r'く$', unicode_string):
        return re.sub(r'く$', u'ける', unicode_string)
    if re.search(r'す$', unicode_string):
        return re.sub(r'す$', u'せる', unicode_string)
    if re.search(r'つ$', unicode_string):
        return re.sub(r'つ$', u'てる', unicode_string)
    if re.search(r'ぶ$', unicode_string):
        return re.sub(r'ぶ$', u'べる', unicode_string)
    if re.search(r'ぬ$', unicode_string):
        return re.sub(r'ぬ$', u'ねる', unicode_string)
    if re.search(r'る$', unicode_string):
        return re.sub(r'る$', u'れる', unicode_string)
    if re.search(r'む$', unicode_string):
        return re.sub(r'む$', u'める', unicode_string)
    if re.search(r'ぐ$', unicode_string):
        return re.sub(r'ぐ$', u'げる', unicode_string)

def utoi(unicode_string):
    if re.search(r'う$', unicode_string):
        return re.sub(r'う$', u'い', unicode_string)
    if re.search(r'く$', unicode_string):
        return re.sub(r'く$', u'き', unicode_string)
    if re.search(r'す$', unicode_string):
        return re.sub(r'す$', u'し', unicode_string)
    if re.search(r'つ$', unicode_string):
        return re.sub(r'つ$', u'ち', unicode_string)
    if re.search(r'ぶ$', unicode_string):
        return re.sub(r'ぶ$', u'び', unicode_string)
    if re.search(r'ぬ$', unicode_string):
        return re.sub(r'ぬ$', u'に', unicode_string)
    if re.search(r'る$', unicode_string):
        return re.sub(r'る$', u'り', unicode_string)
    if re.search(r'む$', unicode_string):
        return re.sub(r'む$', u'み', unicode_string)
    if re.search(r'ぐ$', unicode_string):
        return re.sub(r'ぐ$', u'ぎ', unicode_string)
    
def utoa(unicode_string):
    if re.search(r'う$', unicode_string):
        return re.sub(r'う$', u'わ', unicode_string)
    if re.search(r'く$', unicode_string):
        return re.sub(r'く$', u'か', unicode_string)
    if re.search(r'す$', unicode_string):
        return re.sub(r'す$', u'さ', unicode_string)
    if re.search(r'つ$', unicode_string):
        return re.sub(r'つ$', u'た', unicode_string)
    if re.search(r'ぶ$', unicode_string):
        return re.sub(r'ぶ$', u'ば', unicode_string)
    if re.search(r'ぬ$', unicode_string):
        return re.sub(r'ぬ$', u'な', unicode_string)
    if re.search(r'る$', unicode_string):
        return re.sub(r'る$', u'ら', unicode_string)
    if re.search(r'む$', unicode_string):
        return re.sub(r'む$', u'ま', unicode_string)
    if re.search(r'ぐ$', unicode_string):
        return re.sub(r'ぐ$', u'が', unicode_string)
    
def utoryk(unicode_string):
    if re.search(r'う$', unicode_string):
        return re.sub(r'う$', u'っ', unicode_string)
    if re.search(r'く$', unicode_string):
        return re.sub(r'く$', u'い', unicode_string)
    if re.search(r'す$', unicode_string):
        return re.sub(r'す$', u'し', unicode_string)
    if re.search(r'つ$', unicode_string):
        return re.sub(r'つ$', u'っ', unicode_string)
    if re.search(r'ぶ$', unicode_string):
        return re.sub(r'ぶ$', u'ん', unicode_string)
    if re.search(r'ぬ$', unicode_string):
        return re.sub(r'ぬ$', u'ん', unicode_string)
    if re.search(r'る$', unicode_string):
        return re.sub(r'る$', u'っ', unicode_string)
    if re.search(r'む$', unicode_string):
        return re.sub(r'む$', u'ん', unicode_string)
    if re.search(r'ぐ$', unicode_string):
        return re.sub(r'ぐ$', u'ん', unicode_string)