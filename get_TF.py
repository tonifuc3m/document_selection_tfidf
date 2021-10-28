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

def main(outpath, ANN=pd.DataFrame, labels=[], TF_source={}, target_corpus='', corpus='source'):
    
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
        TF = get_tf_from_dict(TF_source, target_corpus, labels)
        
    # Save TF
    with open(outpath, 'w') as f:
        print(f"Saving Term Frequency in {outpath}...")
        json.dump(TF, f)
    return TF
    
def get_tf_from_ANN(ANN, labels=[]):
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
        Dictionary with term frequencies for every annotation of every label.

    """
    TF = {}
    for label in labels:
        this = ANN.loc[ANN['label']==label, ['span', 'filename']].copy()
        this['norm_str'] = this.apply(lambda x: filter_annotations(_normalize_str(remove_dates(x['span'])), set()), axis=1)
        TF[label] = this.groupby('norm_str')['norm_str'].count().to_dict()
        if False in TF[label].keys():
            TF[label].pop(False)
    return TF
 

def get_tf_from_dict(TF_source={}, txt=[], labels=[]):
    """
    From the entities detected in the source corpus, obtain the term frequency of
    each annotation in the target corpus

    Parameters
    ----------
    txt : str
        New corpus in one string
    labels : list, optional
        List of dict_ labels. The default is []. 
    TF_source : dict
        Dictionary with terms to look. It has as keys, the annotation label. 
        As values, another dictionary, with keys the terms we want to look
    mode : str, optional
        if 'compute', parse ANN and compute TF. If 'retrieve', simply get the 
        already stored TF. The default is 'compute'.

    Returns
    -------
    TF : dict
        Dictionary with term frequencies for every annotation of every label 
        in the new corpus.

    """

    TF = {}
    for label in labels:
        TF_this = {}
        for k in TF_source[label].keys():
            TF_this[k] = txt.count(k)
        TF[label] = TF_this

    return TF