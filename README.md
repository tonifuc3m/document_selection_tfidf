# Document selection based on TF-iDF and a dummy lookup

A script/project to select documents from a target corpus based on their shared vocabulary with a source annotated corpus.


### Installation

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

### Usage
```
python main.py --source-corpus-path SOURCE_PATH --target-corpus-path TARGET_PATH --output-path OUTPUT_PATH --relevant-labels RELEVANT_LABELS 
```

The script main.py executes the entire pipeline. It has the following arguments:

* Source corpus folder (Brat format) (--source-corpus-path)
* Target corpus folder (--target-corpus-path)
* Output folder (--output-path)
* List of relevant labels to consider (--relevant-labels)

