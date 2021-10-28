#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 13:16:48 2021

@author: antonio
"""
import os
import json
import numpy as np

def main(outpath_score1, outpath_score2, outpath_sum_score1, outpath_sum_score2,
         TF_source={}, TF_target={}, iDF_target={}, lookup={}, labels=[], corpus_dict={}):
    
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
        pheno_score1_sum, pheno_score2_sum = \
            sum_scores(pheno_score1=pheno_score1, pheno_score2=pheno_score2, 
                       corpus_dict=corpus_dict, labels=labels)
        # Save aggregated scores
        print(f"Saving aggregated scores in {outpath_sum_score1} and {outpath_sum_score2}...")
        with open(outpath_sum_score1, 'w') as f:
            json.dump(pheno_score1_sum, f)
        with open(outpath_sum_score2, 'w') as f:
            json.dump(pheno_score2_sum, f)
        return pheno_score1_sum, pheno_score2_sum
    
    if (os.path.exists(outpath_score1)) & (os.path.exists(outpath_score2)):
        print(f"Scores already aggregated. \nLoading from {outpath_sum_score1} and {outpath_sum_score2}...")
        with open(outpath_sum_score1, 'r') as f:
            pheno_score1_sum = json.load(f)
        with open(outpath_sum_score2, 'r') as f:
            pheno_score2_sum = json.load(f)
        return pheno_score1_sum, pheno_score2_sum
    
    print("Aggregating scores...")
    pheno_score1_sum, pheno_score2_sum = \
        sum_scores(pheno_score1=pheno_score1, pheno_score2=pheno_score2, 
                   corpus_dict=corpus_dict, labels=labels)
    # Save aggregated scores
    print(f"Saving aggregated scores in {outpath_sum_score1} and {outpath_sum_score2}...")
    with open(outpath_sum_score1, 'w') as f:
        json.dump(pheno_score1_sum, f)
    with open(outpath_sum_score2, 'w') as f:
        json.dump(pheno_score2_sum, f)
    return pheno_score1_sum, pheno_score2_sum
        

def compute_scores(TF_source={}, TF_target={}, iDF_target={}, lookup={}, labels=[]):
    """
    

    Parameters
    ----------
    TF_source : TYPE
        DESCRIPTION
    TF_target : TYPE
        DESCRIPTION
    iDF_target : TYPE
        DESCRIPTION
    labels : TYPE
        DESCRIPTION
    lookup : TYPE
        DESCRIPTION

    Returns
    -------
    score1 : TYPE
        DESCRIPTION.
    score2 : TYPE
        DESCRIPTION.

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
                    if np.log(TF_target[label][k] +1) == 0.0:
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

        
def sum_scores(score1={}, score2={}, corpus_dict={}, labels=[]):
    """
    

    Parameters
    ----------
    score1 : TYPE
        DESCRIPTION
    score2 : TYPE
        DESCRIPTION
    labels : TYPE, optional
        DESCRIPTION. The default is [].


    Returns
    -------
    score1_sum : TYPE
        DESCRIPTION.
    score2_sum : TYPE
        DESCRIPTION.


    """
    
    score1_sum = {}
    score2_sum = {}
    for doc_name in score1.keys():
        s_and_d_1 = []
        s_and_d_2 = []
        length_normalization = len(corpus_dict[doc_name].split())
        for label in labels:    
            s_and_d_1 = s_and_d_1 + score1[doc_name][label]
            s_and_d_2 = s_and_d_2 + score2[doc_name][label]
        score1_sum[doc_name] = sum(s_and_d_1)/length_normalization
        score2_sum[doc_name] = sum(s_and_d_2)/length_normalization

    return score1_sum, score2_sum