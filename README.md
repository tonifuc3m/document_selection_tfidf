# Document selection based on TF-iDF and a dummy lookup

<p align="left">
    <br />
    <a href="https://github.com/tonifuc3m/document_selection_tfidf/"><strong>Explore the docs »</strong></a>
</p>

A library to select documents from a target corpus based on their shared vocabulary with a source annotated corpus.

 + **Problem statement**. I want to determine which documents of my corpus belong to a given domain X (e.g. biomedicine, law, informatics, etc.) 

 + **Input**. 2 corpus (source and target). The *source* corpus has entity annotations and all its documents belong to the domain X. The *target* corpus has only the plain documents and it contains documents from miscellaneous sources.

 + **Output**. A ranking of *target* documents according to their membership to the domain X.


<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Installation">Installation</a>
    </li>
    <li>
      <a href="#Usage">Usage</a>
    </li>
    <li>
      <a href="#Algorithm overview">Algorithm overview</a>
    </li>
  </ol>
</details>

<!-- Installation -->
## Installation

1. Clone the repo

   ```sh
   git clone https://github.com/tonifuc3m/document_selection_tfidf.git
   cd document_selection_tfidf
   git clone https://github.com/tonifuc3m/utils_BSC.git
   ```

2. Create a new virtual environment

   ```sh
   python3 -m venv .env
   ```

3. Activate the new environment

   ```sh
   source .env/bin/activate
   ```

4. Install the requirements

    ```sh
    python -m pip install pandas
    python -m pip install kneed
    ```

## Usage
```
python main.py --source-corpus-path SOURCE_PATH --target-corpus-path TARGET_PATH --output-path OUTPUT_PATH --relevant-labels RELEVANT_LABELS 
```

The script main.py executes the entire pipeline. It has the following arguments:

* Source corpus folder (Brat format) (--source-corpus-path)
* Target corpus folder (one text file per document) (--target-corpus-path)
* Output folder (--output-path)
* List of relevant labels to consider (--relevant-labels)


## Algorithm overview

1. Generate entity gazetteers from the *source* corpus. One gazetteer is generated per entity label.

2. Execute a lookup of the gazetteers on the *target* corpus.

3. Compute the log(term frequency) of every annotation in the *source* and *target* corpora.

4. Compute the inverse document frequency of every annotation in the *target* corpus.

5. Compute, for every annotation, two scores:

+ score1 = TFsource / TFtarget

+ score2 = TFsource * iDFtarget

Now, for every *target* document, we have two scoring arrays. 

6. Compute the ranking of every target document according to the scores (the document with the highest score is ranked as 1, the second one as 2, etc.).
Now, for every case report, we have two rankings. 

7. Average them to obtain the median ranking.



<p align="center">
    <a href="https://github.com/tonifuc3m/document_selection_tfidf/issues">Report Bug</a>
    ·
    <a href="https://github.com/tonifuc3m/document_selection_tfidf/issues">Request Feature</a>
</p>

