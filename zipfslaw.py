#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 15:31:24 2021

@author: antonio
https://www.codedrome.com/zipfs-law-in-python/
"""
import collections


def generate_zipf_table(text, top):

    """
    Create a list of dictionaries containing the top
    most frequent words, their frequencies and
    other Zipfian data.
    """

    # text = _remove_punctuation(text)

    text = text.lower()

    top_word_frequencies = _top_word_frequencies(text, top)

    zipf_table = _create_zipf_table(top_word_frequencies)

    return zipf_table


def _remove_punctuation(text):

    """
    Removes the characters:
    !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~0123456789
    from the text.
    """

    chars_to_remove = "!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~0123456789"

    tr = str.maketrans("", "", chars_to_remove)

    return text.translate(tr)


def _top_word_frequencies(text, top):

    """
    Create a list of tuples containing the most
    frequent words and their frequencies
    in descending order.
    """

    # With no argument, split() separates the string
    # by 1 or more consecutive instances of whitespace.
    words = text.split()

    # Create a collections.Counter instance from an
    # iterable, in this case our list of words.
    word_frequencies = collections.Counter(words)

    # most_common() gives us a list of tuples
    # containing words and their frequencies,
    # in descending order of frequency.
    top_word_frequencies = word_frequencies.most_common(top)

    return top_word_frequencies


def _create_zipf_table(frequencies):

    """
    Takes the list created by _top_word_frequencies
    and inserts it into a list of dictionaries,
    along with the Zipfian data.
    """

    zipf_table = []

    top_frequency = frequencies[0][1]

    for index, item in enumerate(frequencies, start=1):

        relative_frequency = "1/{}".format(index)
        zipf_frequency = top_frequency * (1 / index)
        difference_actual = item[1] - zipf_frequency
        difference_percent = (item[1] / zipf_frequency) * 100

        zipf_table.append({"word": item[0],
                           "actual_frequency": item[1],
                           "relative_frequency": relative_frequency,
                           "zipf_frequency": zipf_frequency,
                           "difference_actual": difference_actual,
                           "difference_percent": difference_percent})

    return zipf_table


def print_zipf_table(zipf_table):

    """
    Prints the list created by generate_zipf_table
    in table format with column headings.
    """

    width = 80

    print("-" * width)
    print("|Rank|    Word    |Actual Freq | Zipf Frac  | Zipf Freq  |Actual Diff |Pct Diff|")
    print("-" * width)

    format_string = "|{:4}|{:12}|{:12.0f}|{:>12}|{:12.2f}|{:12.2f}|{:7.2f}%|"

    for index, item in enumerate(zipf_table, start=1):

        print(format_string.format(index,
                                   item["word"],
                                   item["actual_frequency"],
                                   item["relative_frequency"],
                                   item["zipf_frequency"],
                                   item["difference_actual"],
                                   item["difference_percent"]))

    print("-" * width)
    
    
import numpy as np
from matplotlib import pyplot as plt
import os
def zipfs(TF, outpath_general, labels):
    for label in labels:
        zipfstable = generate_zipf_table(' '.join(TF[label]), 
                                         len(set(TF[label])))
        logrank = []
        logfreq = []
        for index, item in enumerate(zipfstable, start=1):
            logrank.append(np.log(index))
            logfreq.append(np.log(item['actual_frequency']))
        fig = plt.figure(1)         # create a figure instance
        ax = fig.add_subplot(111)   # and axes
        ax.plot(logrank, logfreq)
        plt.ylabel('Log Freq')
        plt.xlabel('Log Rank')
        plt.title(f'Zipfs plot {label}')
        # plt.show()                # this would show the plot, but you can leave it out 
        plt.tight_layout()
        os.makedir(os.path.join(outpath_general, 'zipfs-laws'))
        fig.savefig(os.path.join(outpath_general, 'zipfs-laws', f'{label}.png'),
                    dpi = 500)
        plt.clf()