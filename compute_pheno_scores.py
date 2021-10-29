#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 13:16:48 2021

@author: antonio
"""
import os
import json
import numpy as np

def main(outpath_score1: str, outpath_score2: str, outpath_sum_score1: str,
         outpath_sum_score2: str, TF_source={}, TF_target={}, iDF_target={},
         lookup={}, labels=[], corpus_dict={}):
    """
    

    Parameters
    ----------
    outpath_score1 : str
        DESCRIPTION.
    outpath_score2 : str
        DESCRIPTION.
    outpath_sum_score1 : str
        DESCRIPTION.
    outpath_sum_score2 : str
        DESCRIPTION.
    TF_source : dict, optional
        Dictionary with key: text spans (str), value: another dict with theh 
        term frequencies (int) in the source corpus, grouped by label (keys).
        The default is {}.
    TF_target : dict, optional
        Dictionary with key: text spans (str), value: another dict with the 
        term frequencies (int) in the target corpus, grouped by label (keys).
        The default is {}.
    iDF_target : dict, optional
        Dictionary with key: annotation label (str), value: another dict with the 
        inverse document frequencies in the target corpus (value, float), of
        every annotation text span (key, str). The default is {}.
    lookup : dict, optional
        Dictionary with key: document name, value: another dict with the 
        list of the annotations present in the document, groupby by label (key).
        The default is {}.
    labels : dict, optional
        Labels we parse from annotations. Annotations in the dictionaries are
        grouped by label. The default is [].
    corpus_dict : dict, optional
        Dictionary with the corpus. Key: document name, value: string with
        document content. The default is {}.

    Returns
    -------
    pheno_score1_sum : dict
        Dictionary with the aggregated scores 1. Key: document name, 
        value: another dict with the final score (floats) grouped by label.
    pheno_score2_sum : dict
        Dictionary with the aggregated scores 2. Key: document name, 
        value: another dict with the final score (floats) grouped by label.

    """
    
    # Compute scores for every entity
    exist_sc = False
    if (os.path.exists(outpath_score1)) & (os.path.exists(outpath_score2)):
        print(f"Scores JSON already exist. \nLoading from {outpath_score1} and {outpath_score2}...")
        exist_sc=True
        with open(outpath_score1, 'r') as f:
            pheno_score1 = json.load(f)
        with open(outpath_score2, 'r') as f:
            pheno_score2 = json.load(f)
            
    else:
        print("Computing scores...")
        pheno_score1, pheno_score2 = \
            compute_scores(TF_source=TF_source, TF_target=TF_target, 
                           iDF_target=iDF_target, lookup=lookup, labels=labels)
        # Save scores
        print(f"Saving scores in {outpath_score1} and {outpath_score2}...")
        with open(outpath_score1, 'w') as f:
            json.dump(pheno_score1, f)
        with open(outpath_score2, 'w') as f:
            json.dump(pheno_score2, f)
            
    # Combine scores
    if (exist_sc==False):
        print("Aggregating scores...")
        pheno_score1_sum = sum_scores(score=pheno_score1, corpus_dict=corpus_dict,
                                      labels=labels)
        del pheno_score1
        pheno_score2_sum = sum_scores(score=pheno_score2, corpus_dict=corpus_dict,
                                      labels=labels)
        del pheno_score2

        # Save aggregated scores
        print(f"Saving aggregated scores in {outpath_sum_score1} and {outpath_sum_score2}...")
        with open(outpath_sum_score1, 'w') as f:
            json.dump(pheno_score1_sum, f)
        with open(outpath_sum_score2, 'w') as f:
            json.dump(pheno_score2_sum, f)
        return pheno_score1_sum, pheno_score2_sum
    
    if (os.path.exists(outpath_sum_score1)) & (os.path.exists(outpath_sum_score2)):
        print(f"Scores already aggregated. \nLoading from {outpath_sum_score1} and {outpath_sum_score2}...")
        with open(outpath_sum_score1, 'r') as f:
            pheno_score1_sum = json.load(f)
        with open(outpath_sum_score2, 'r') as f:
            pheno_score2_sum = json.load(f)
        return pheno_score1_sum, pheno_score2_sum
    
    print("Aggregating scores...")
    pheno_score1_sum = sum_scores(score=pheno_score1, corpus_dict=corpus_dict,
                                  labels=labels)
    del pheno_score1
    pheno_score2_sum = sum_scores(score=pheno_score2, corpus_dict=corpus_dict,
                                  labels=labels)
    del pheno_score2
    # Save aggregated scores
    print(f"Saving aggregated scores in {outpath_sum_score1} and {outpath_sum_score2}...")
    with open(outpath_sum_score1, 'w') as f:
        json.dump(pheno_score1_sum, f)
    with open(outpath_sum_score2, 'w') as f:
        json.dump(pheno_score2_sum, f)
    return pheno_score1_sum, pheno_score2_sum
        

def compute_scores(TF_source: dict, TF_target: dict, iDF_target: dict, 
                   lookup: dict, labels: list):
    """
    Compute the scores for each document. 
    
    Score 1 = log(TFsource+1)/ log(TFtarget+1)
    Score 2 = log(TFsource+1) * iDF
    
    Every document will have a list of scores per label. The list length is the
    number of annotations in the source corpus.
    Example: 
        TF source: diabetes: 10, diarrhea: 10, headache: 5. 
        TF target document: diarrhea: 1, headache: 1. 
        
        Score1 for target document = [0, 3.46, 2.58]

    Parameters
    ----------
    TF_source : dict
        Dictionary with key: text spans (str), value: another dict with theh 
        term frequencies (int) in the source corpus, grouped by label (keys)
    TF_target : dict
        Dictionary with key: text spans (str), value: another dict with the 
        term frequencies (int) in the target corpus, grouped by label (keys)
    iDF_target : dict
        Dictionary with key: annotation label (str), value: another dict with the 
        inverse document frequencies in the target corpus (value, float), of
        every annotation text span (key, str).
    labels : list
        Labels we parse from annotations. Annotations in the dictionaries are
        grouped by label
    lookup : dict
        Dictionary with key: document name, value: another dict with the 
        list of the annotations present in the document, groupby by label (key)

    Returns
    -------
    score1 : dict
        Dictionary with key: document name, value: another dict with lists of
        scores, one per each term, grouped by label. If a given term is not 
        present in the document, the score is 0 
        Score 1 = log(TFsource+1)/ log(TFtarget+1)
    score2 : dict
        Dictionary with key: document name, value: another dict with lists of
        scores, one per each term, grouped b label. If a given term is not 
        present in the document, the score is 0 
        Score = log(TFsource+1) * iDF

    """

    score1 = {}
    score2 = {}
    c = 0
    for cc in lookup.keys():
        c += 1
        # print(c/len(all_txt))
        score1_per_doc = {}
        score2_per_doc = {}
        for label in labels:
            score1_this = []
            score2_this = []
            for k in sorted(TF_source[label].keys()):
                if k in lookup[cc][label]:
                    if np.log(TF_target[label][k] +1) == 0.0: # TODO: Safety if clause. This should never happend because if the previous if clause. Remove it
                        print(cc, label, k)
                    score1_this.append(np.log(TF_source[label][k] +1) / np.log(TF_target[label][k] +1))
                    score2_this.append(np.log(TF_source[label][k] +1) * iDF_target[label][k])
                else:
                    score1_this.append(0)
                    score2_this.append(0)
            score1_per_doc[label] = score1_this
            score2_per_doc[label] = score2_this
        score1[cc] = score1_per_doc
        score2[cc] = score2_per_doc

    return score1, score2

        
def sum_scores(score: dict, corpus_dict: dict, labels: list):
    """
    Aggregate scores per document. Sum them and divide by the document length

    Parameters
    ----------
    score : dict
        Dictionary with key: document name, value: another dict with lists of
        scores, one per each term, grouped by label. If a given term is not 
        present in the document, the score is 0 
    corpus_dict : dict
        Dictionary with the corpus. Key: document name, value: string with
        document content.
    labels : list
        Labels we parse from annotations.

    Returns
    -------
    score_sum : dict
        Dictionary with the aggregated scores. Key: document name, 
        value: another dict with the final score (floats) grouped by label.

    """
    
    score_sum = {}
    for doc_name in score.keys():
        s_and_d = []
        length_normalization = len(corpus_dict[doc_name].split())
        for label in labels:    
            s_and_d = s_and_d + score[doc_name][label]
        score_sum[doc_name] = sum(s_and_d)/length_normalization

    return score_sum