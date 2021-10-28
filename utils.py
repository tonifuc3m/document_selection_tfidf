#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 12:36:15 2021

@author: antonio
"""
import re
import string
import os


beg_pattern='*#-:=.,)/% '
end_pattern=':=.,(/%!? '

def _normalize_str(_string_, beg_pattern='"*#-:=.,)/% ', end_pattern='"":=.,(/%!? ', min_upper=4):
    '''
    (1) Lowercase 
    (2) Remove extra whitespaces from given string
    (3) Remove leading and trailing characters
    '''
    # Lowercase
    string_lower = ' '.join(list(map(lambda x: x.lower() if len(x)>min_upper 
                                     else x, _string_.split(' '))))
    # Remove whitespaces
    str_bs = re.sub('\s+', ' ', string_lower).strip()
    
    # Remove leading and trailing characters
    str_bs = str_bs.rstrip(end_pattern)
    str_bs = str_bs.lstrip(beg_pattern)
    
    return str_bs

def remove_trailing_doses(_string_):
    _string_ = re.sub("[0-9]*mg\/.*", "", _string_)
    _string_ = re.sub("[0-9]*[a-zA-Z]*\/.*h", "", _string_)
    _string_ = re.sub("[0-9]*\/.*g", "", _string_)
    _string_ = re.sub("[0-9]*g", "", _string_)
    return _string_

    
def remove_dates(_string_):
    _string_ = re.sub("[0-9]*\/[0-9]*","", _string_)
    _string_ = re.sub("[0-9]*\/[0-9]*","", _string_)
    _string_ = re.sub("[0-9]*\.[0-9]*","", _string_)
    _string_ = re.sub("[0-9]*\.[0-9]*","", _string_)
    return _string_

count_punct = lambda l1,l2: sum([1 for x in l1 if x in l2])
count_alpha = lambda x: sum([1 for c in x if c.isalpha()])

def filter_annotations(_string_, stpw):

    l = len(_string_)
    if l<=1: # Length is lower than 2, skip
        return False
    
    # Length is <2 without counting punctuation, skip
    l_non_punct = l-count_punct(_string_,set(string.punctuation)) 
    if l_non_punct<2: # Length is <2 without counting punctuation, skip
        return False
    
    # No alphabetic characters, skip
    num_alpha = count_alpha(_string_)
    if num_alpha<1: 
        return False
    
    # Remove annotations that are just a stopword
    if len(set([_string_]).intersection(stpw))>0: 
        return False
    
    return _string_

def load_corpus(path):
    print(f"Loading corpus from {path}...")
    corpus_dict = {}
    for txt in os.listdir(path):
        if '.txt' not in txt:
            continue
        corpus_dict[txt] = _normalize_str(open(os.path.join(path, txt)).read(), min_upper=5)
    all_txt_cat =  " ". join([str(text) for text in corpus_dict.values()])
    
    return corpus_dict, all_txt_cat