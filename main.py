#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 12:27:54 2021

@author: antonio
Main
"""
from utils_BSC.parse import parse_ann
import get_TF
import get_iDF
import compute_pheno_scores
from utils import load_corpus
import os
from zipfslaw import zipfs
import select_documents
import argparse

def argarser():
    parser = argparse.ArgumentParser(description='process user given parameters')
    parser.add_argument("--source-corpus-path", required = True, dest = "source_path", 
                        help = "Path source corpus with annotations in Brat")
    parser.add_argument("--target-corpus-path", required = True, dest = "target_path", 
                        help = "Path to target corpus")
    parser.add_argument("--output-path", required =  True, dest="output_path", 
                        help = "Path to output folder")
    parser.add_argument("--relevant-labels", required = True, dest="relevant_labels", 
                        nargs = '+', help = "Brat labels")
    
    args = parser.parse_args()
    
    source_path = args.source_path
    target_path = args.target_path
    output_path = args.output_path
    relevant_labels = args.relevant_labels
    
    return source_path, target_path, output_path, relevant_labels
    
def compute_metrics(source_path: str, target_path: str, outpath_general: str, relevant_labels: list):
    """
    

    Parameters
    ----------
    source_path : str
        Path to source annotated corpus in Brat standoff format.
    target_path : str
        Path to target corpus.
    outpath_general : str
        Output folder where we will store all variables.
    relevant_labels : list
        Labels we parse from annotations.

    Returns
    -------
    None.

    """
    # Parse NER output
    ANN = parse_ann(source_path, labels_to_ignore = [], with_notes=False)
    ANN = ANN.loc[ANN['label'].isin(relevant_labels)==True,:].copy()
    
    # Get Term Frequency in original corpus
    TF_source_outpath = os.path.join(outpath_general, 'TF_source.json')
    TF_source = get_TF.main(TF_source_outpath, ANN=ANN, labels=relevant_labels,
                            corpus='source')
    
    zipfs_bool = input("Do you want to compute the Zipf's law? (Y/N) ")
    if zipfs_bool=='Y':
        print(f"Zipfs figures stored in {os.path.join(outpath_general, 'zipfs-laws')}")
        zipfs(TF_source, outpath_general, relevant_labels)
        
    # Load target corpus
    corpus_dict, _ = load_corpus(target_path)
    
    # Get TF in source corpus
    TF_target_outpath = os.path.join(outpath_general, 'TF_target.json')
    TF_target = get_TF.main(TF_target_outpath, labels=relevant_labels, TF_source=TF_source,
                            target_corpus=corpus_dict, corpus='target')
    
    # Get iDF
    iDF_outpath = os.path.join(outpath_general, 'iDF_target.json')
    count_outpath = os.path.join(outpath_general, 'count_target.json')
    lookup_outpath = os.path.join(outpath_general, 'lookup.json')
    iDF, lookup = get_iDF.main(outpath_idf=iDF_outpath, outpath_count=count_outpath,
                       outpath_lookup=lookup_outpath, corpus_dict=corpus_dict,
                       labels=relevant_labels, TF_source=TF_source)
    
    # Compute scores
    outpath_score1 = os.path.join(outpath_general, 'score1.json')
    outpath_score2 = os.path.join(outpath_general, 'score2.json')
    outpath_sum_score1 = os.path.join(outpath_general, 'score1_sum.json')
    outpath_sum_score2 = os.path.join(outpath_general, 'score2_sum.json')
    pheno_score1_sum, pheno_score2_sum = \
        compute_pheno_scores.main(outpath_score1, outpath_score2, outpath_sum_score1,
                              outpath_sum_score2, TF_source=TF_source, 
                              TF_target=TF_target, iDF_target=iDF, lookup=lookup,
                              labels=relevant_labels, corpus_dict=corpus_dict)
    
    
if __name__ == '__main__':

    # Parse arguments
    source_path, target_path, outpath_general, relevant_labels = argarser()

    
    # Compute metrics
    compute_metrics(source_path, target_path, outpath_general, relevant_labels)
    
    # Find relevant documents
    select_documents.main(os.path.join(outpath_general, 'score1_sum.json'), 
                          outpath_general, 'top', top=12580)

