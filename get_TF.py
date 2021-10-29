#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 12:40:19 2021

@author: antonio
Get Term Frequency
"""
import os
import json
import pandas as pd
from utils import filter_annotations, _normalize_str, remove_dates

def main(outpath: str, ANN=pd.DataFrame, labels=[], TF_source={}, 
         target_corpus_dict={}, corpus='source'):
    """
    

    Parameters
    ----------
    outpath : str
        DESCRIPTION.
    ANN : pandas DataFrame, optional
        DESCRIPTION. The default is pd.DataFrame.
    labels : list, optional
        DESCRIPTION. The default is [].
    TF_source : TYPE, optional
        Dictionary with key: annotation label (str), value: another dict with the 
        term frequencies in the source string (value, float), of every 
        annotation text span (key, str). The default is {}.
    target_corpus_dict : dict, optional
        DESCRIPTION. The default is {}.
    corpus : str, optional
        Corpus we are getting the TF from. Either 'source' or 'target'.
        The default is 'source'.

    Returns
    -------
    TF : TYPE
        DESCRIPTION.

    """
    if corpus not in ['target', 'source']:
        raise ValueError("Wrong 'corpus' argument value. It must be either " +
                         "'target' or 'source'")
    # If TF is already saved, load it
    if os.path.exists(outpath):
        print(f"Term Frequency JSON already exists. \nLoading from {outpath}...")
        with open(outpath, 'r') as f:
            TF = json.load(f)
        return TF
    
    # Compute TF
    if corpus=='source':
        print("Computing Term Frequency from Annotations DataFrame (source)...")
        TF = get_tf_from_ANN(ANN, labels=labels)
    elif corpus=='target':
        print("Computing Term Frequency from dictionary (target)...")
        target_corpus =  " ". join([str(text) for text in target_corpus_dict.values()])
        TF = get_tf_from_dict(TF_source, target_corpus, labels)
        
    # Save TF
    with open(outpath, 'w') as f:
        print(f"Saving Term Frequency in {outpath}...")
        json.dump(TF, f)
    return TF
    
def get_tf_from_ANN(ANN, labels: list):
    """
    From a pandas DataFrame with ANN annotations, obtain the term frequency of
    each annotation

    Parameters
    ----------
    ANN : pandas DataFrame 
        It has information from ANN files. Columns: 'annotator', 'bunch',
        'filename', 'mark', 'label', 'offset1', 'offset2', 'span', 'code'
    labels : list
        List of ANN labels

    Returns
    -------
    TF : dict
        Dictionary with key: annotation label (str), value: another dict with the 
        term frequencies in the corpus (value, float), of every annotation text
        span (key, str).

    """
    TF = {}
    for label in labels:
        this = ANN.loc[ANN['label']==label, ['span', 'filename']].copy()
        this['norm_str'] = this.apply(lambda x: filter_annotations(_normalize_str(remove_dates(x['span'])), set()), axis=1)
        TF[label] = this.groupby('norm_str')['norm_str'].count().to_dict()
        if False in TF[label].keys():
            TF[label].pop(False)
    return TF
 

def get_tf_from_dict(TF_source: dict, txt: str, labels: list):
    """
    From the entities detected in the source corpus, obtain the term frequency of
    each annotation in a text string

    Parameters
    ----------
    txt : str
        New corpus in one string
    labels : list
        List of annotation labels.
    TF_source : dict
        Dictionary with key: annotation label (str), value: another dict with the 
        term frequencies in the source string (value, float), of every 
        annotation text span (key, str).
    mode : str, optional
        if 'compute', parse ANN and compute TF. If 'retrieve', simply get the 
        already stored TF. The default is 'compute'.

    Returns
    -------
    TF : dict
        Dictionary with key: annotation label (str), value: another dict with the 
        term frequencies in the txt string (value, float), of every annotation text
        span (key, str).

    """

    TF = {}
    for label in labels:
        TF_this = {}
        for k in TF_source[label].keys():
            TF_this[k] = txt.count(k)
        TF[label] = TF_this

    return TF