#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 12:59:57 2021

@author: antonio
Get iDF
"""
import numpy as np
import os
import json


def main(outpath_idf='', outpath_count='', outpath_lookup='', corpus_dict={}, labels=[], TF_source={}):
    
    # Lookup
    if os.path.exists(outpath_lookup):
        print(f"Lookup JSON already exists. \nLoading from {outpath_lookup}...")
        with open(outpath_lookup, 'r') as f:
            lookup = json.load(f)
    else:
        print("Computing lookup...")
        lookup = dummy_lookup(corpus_dict, labels, TF_source)
    
        # Save lookup
        print(f"Saving lookup in {outpath_lookup}...")
        with open(outpath_lookup, 'w') as f:
            json.dump(lookup, f)
        
    # Compute iDF
    if os.path.exists(outpath_idf):
        print(f"Inverse Document Frequency JSON already exists. \nLoading from {outpath_idf}...")
        with open(outpath_idf, 'r') as f:
            iDF = json.load(f)
        return iDF
    else: 
        print("Computing inverse Document Frequency...")
        iDF, n_docs_with_term = get_idf(TF_source=TF_source, corpus_dict=corpus_dict, labels=labels)
        
        # Save iDF 
        print(f"Saving inverse Document Frequency in {outpath_idf}...")
        with open(outpath_idf, 'w') as f:
            json.dump(iDF, f)
        print(f"Saving document count in {outpath_count}...")
        with open(outpath_count, 'w') as f:
            json.dump(n_docs_with_term, f)
    
    return iDF, lookup
    
    

def dummy_lookup(docs_dict={}, labels=[], TF_source={}):
    """
    Perform dummiest lookup on new corpus

    Parameters
    ----------
    docs_dict : dict, optional
        Dictionary with new corpus (keys are file name, values are the content)
        . The default is {}.
    labels : list, optional
        DESCRIPTION. The default is [].
    TF_source : TYPE, optional
        DESCRIPTION. The default is {}.


    Returns
    -------
    lookup : TYPE
        DESCRIPTION.

    """
    lookup = {}
    c = 0
    for doc_name, txt in docs_dict.items():
        c += 1
        # print(c/len(all_txt))
        lookup_label = {}
        for label in labels:
            lookup_this = []
            for k in set(TF_source[label].keys()):
                if k in txt:
                    lookup_this.append(k)
            lookup_label[label] = lookup_this
        lookup[doc_name] = lookup_label
    return lookup



def get_idf(TF_source={}, corpus_dict={}, labels = []):
    """
    Get inverse Document Frequency of source entities on new corpus

    Parameters
    ----------
    TF_source : TYPE, optional
        DESCRIPTION. The default is {}.
    corpus_dict : dict, optional
        Dictionary with new corpus (keys are file name, values are the content)
        . The default is {}.
    labels : list, optional
        DESCRIPTION. The default is [].


    Returns
    -------
    iDF : TYPE
        DESCRIPTION.
    n_docs_with_term : dict
        DESCRIPTION
    
    """
    
    # Get lookup
    n_docs = len(corpus_dict.keys())
    iDF = {}
    n_docs_with_term = {}
    for label in labels:
        print(label, len(TF_source[label].keys()))
        iDF_this = {}
        n_docs_with_term_this = {}
        for k in set(TF_source[label].keys()):
            x = sum([k in txt for txt in set(corpus_dict.values())])
            n_docs_with_term_this[k] = x
            iDF_this[k] = -np.log((1+x) / n_docs)
        iDF[label] = iDF_this
        n_docs_with_term[label] = n_docs_with_term_this
    return iDF, n_docs_with_term
