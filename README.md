# BiasWord-Task
## Descrioption
In this project, first, we crawl articles from The Guardians newspaper website. After Cleaning raw data and removing punctuation marks, we use this data to create the Word2Vec model to get similar words to our predefined bias target words. Then the cosine distance along with similar words will be printed for each target word.

# Usage
## Manual:
Install requirements using the following command
```bash
pip install -r requirements.txt
```
Then call the following methods.
```bash
from guardians_article_crawler import create_guardians_dataset
from tokenization import read_model_and_get_similar_words, print_similarity_table, clean_data_and_create_model

targetwords = ['refugee', 'racism', 'nationalism', 'hoax', 'dictator', 'dumb', 'shocked', 'fanatical', 'nasty', 'bigot']
# Crawl articles from Guardians website
path = create_guardians_dataset(path='./', articleCount=4000, category='world')
# Creating Word2Vec model
model = clean_data_and_create_model(dataPath=path, modelPath='./MyModel.model')
# Loading model and getting similar words
similarwords, distances = read_model_and_get_similar_words(modelPath='./MyModel.model', numberOfSimilarWords=100,
                                                           targetWords=targetwords)
# Print(similarwords)
print_similarity_table(targetwords, similarwords, distances)

```

These methods could be found in main.py file.

## Google Colab:
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/17_MOW2twRb5dWj3z3nXEL0ldppHXvLDY)

# Note
Crawling articles, cleaning data and creating the model is time-consuming. You can download and use the dataset, cleaned-dataset and model from [Here](https://drive.google.com/drive/folders/1cTISKzvJfAb9i0JBPpWcLo7pQtRTts1r).
