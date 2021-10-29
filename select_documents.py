#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 14:58:59 2021

@author: antonio
Select Documents
"""
from matplotlib import pyplot as plt
from kneed import KneeLocator
import json
import numpy as np


def elbow_find_relevant_docs(score: dict):
    """
    Elbow method to know which are the most relevant case reports based on their 
    score

    Parameters
    ----------
    score : dict
        key: filename, value: score (float).

    Returns
    -------
    best_N : list
        list of ordered touples with filename and score

    """
    # Plot all
    n_docs = 12580
    l = [score[x] for x in sorted(score, key=score.get, reverse=True)[:n_docs]]

    plt.plot(l)
    plt.savefig('tmp.png')
    
    cutoff1 =int(input('First cutoff (see figure tmp.png): '))
    
    # Select best N ignoring almost zero entriees
    l2 = [score[x] for x in sorted(score, key=score.get, reverse=True)[:cutoff1]]
    i = np.arange(len(l2))
    knee = KneeLocator(i, l2, S=1, curve='convex', direction='decreasing', interp_method='polynomial')
    fig = plt.figure(figsize=(5, 5))
    knee.plot_knee()
    
    # Best N according to ph_score1_symptoms
    best_N = sorted(score, key=score.get, reverse=True)[:knee.knee]
    best_N = [(x, score[x]) for x in best_N]
    return best_N

def main(score_path: str, outpath: str, type_: str, top=0):
    """
    

    Parameters
    ----------
    score_path : str
        Path to JSON with scores per document.
    outpath : str
        Path to output folder.
    type_ : str, optional
        Type of method to select the best scores. Either 'elbow' or 'top'.
    top : int, optional
        Number of top documents to select. The default is 0.

    Returns
    -------
    None.

    """
    
    if type_ not in ['elbow', 'top']:
        raise ValueError("Wrong 'type_' argument value. It must be either " +
                         "'elbow' or 'top'")
        
    # Load scores
    with open(score_path, 'r') as f:
        score = json.load(f)
        
    # Find best documents by score
    if type_ == 'elbow':
        BestN = elbow_find_relevant_docs(score)
    elif type_ == 'top':
        BestN = sorted(score, key=score.get, reverse=True)[:top]
        BestN = [(x, score[x]) for x in BestN]
    # s1_doc = set([x[0] for x in BestN])
    
    # Save document names sorted by score
    with open(outpath, 'w') as fout:
        for item in BestN:
            fout.write(f"{item[0]}\t{item[1]}\n")
        
