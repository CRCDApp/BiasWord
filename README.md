# BiasWord-Task
## Descrioption
In this project, first we crawl articles from The Guardians newspaper website.
After Cleaning raw data and removing punctuation marks, We will use this data to create Word2Vec model to get similar words to our predefined bias target words.
Then the cosine distance along with similar words will be printed for each target words.

# How to Use
## Manual:
Install the following package
```bash
pip install -r requirements.txt
```
Then call the following methods.
```bash
from guardians_article_crawler import create_guardians_dataset
from tokenization import read_model_and_get_similar_words, print_similarity_table, clean_data_and_create_model

targetwords = ['shocked', 'fake']
# Crawl articles from Guardians website
path = create_guardians_dataset(path='./', articleCount=200, category='world')
# Creating Word2Vec model
model = clean_data_and_create_model(dataPath=path, modelPath='./MyModel.model')
# Loading model and getting similar words
similarwords, distances = read_model_and_get_similar_words(modelPath='./MyModel.model', numberOfSimilarWords=3,
                                                           targetWords=targetwords)
# Print(similarwords)
print_similarity_table(targetwords, similarwords, distances)

```

These methods could be found in main.py file.

## Google Colab
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb)
