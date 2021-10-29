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


def main(outpath_idf: str, outpath_count: str, outpath_lookup: str, 
         corpus_dict={}, labels=[], TF_source={}):
    """
    

    Parameters
    ----------
    outpath_idf : str
        Path where to store JSON file with iDF.
    outpath_count : str
        Path where to store JSON file with document count
    outpath_lookup : str
        Path where to store JSON file with lookup
    corpus_dict : dict, optional
        Dictionary with the corpus. Key: document name, value: string with
        document content. The default is {}.
    labels : list, optional
        List of annotation labels. The default is [].
    TF_source : dict, optional
        Dictionary with key: annotation label (str), value: another dict with the 
        term frequencies in the source string (value, float), of every 
        annotation text span (key, str).. The default is {}.

    Returns
    -------
    iDF : dict
        Dictionary with key: annotation label (str), value: another dict with the 
        inverse document frequencies in the target corpus (value, float), of
        every annotation text span (key, str).
    lookup : dict
        Dictionary with key: document name, value: another dict with the 
        list of the annotations present in the document, groupby by label (key).

    """
    
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
        return iDF, lookup
    else: 
        print("Computing inverse Document Frequency...")
        iDF, n_docs_with_term = get_idf(TF_source=TF_source, 
                                        corpus_dict=corpus_dict, labels=labels)
        
        # Save iDF 
        print(f"Saving inverse Document Frequency in {outpath_idf}...")
        with open(outpath_idf, 'w') as f:
            json.dump(iDF, f)
        print(f"Saving document count in {outpath_count}...")
        with open(outpath_count, 'w') as f:
            json.dump(n_docs_with_term, f)
    
    return iDF, lookup
    
    

def dummy_lookup(corpus_dict: dict, labels: list, TF_source: dict):
    """
    Perform dummiest lookup on new corpus

    Parameters
    ----------
    corpus_dict : dict
        Dictionary with the corpus. Key: document name, value: string with
        document content.
    labels : list
        Labels we parse from annotations. Annotations in the dictionaries are
        grouped by label.
    TF_source : dict
        Dictionary with key: annotation label (str), value: another dict with the 
        term frequencies in the source string (value, float), of every 
        annotation text span (key, str).

    Returns
    -------
    lookup : dict
        Dictionary with key: document name, value: another dict with the 
        list of the annotations present in the document, groupby by label (key).

    """
    lookup = {}
    c = 0
    for doc_name, txt in corpus_dict.items():
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



def get_idf(TF_source: dict, corpus_dict: dict, labels: list):
    """
    Get inverse Document Frequency of source entities on new corpus


    Parameters
    ----------
    TF_source : dict
        Dictionary with key: annotation label (str), value: another dict with the 
        term frequencies in the source string (value, float), of every 
        annotation text span (key, str).
    corpus_dict : dict
        Dictionary with the corpus. Key: document name, value: string with
        document content.
    labels : list
        Labels we parse from annotations. Annotations in the dictionaries are
        grouped by label.

    Returns
    -------
    iDF : dict
        Dictionary with key: annotation label (str), value: another dict with the 
        inverse document frequencies in the target corpus (value, float), of
        every annotation text span (key, str)
    n_docs_with_term : dict
        Dictionary with key: annotation label (str), value: another dict with the 
        number of documents in the target corpus (value, int), of every 
        annotation text span (key, str)

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
