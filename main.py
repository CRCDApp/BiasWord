from guardians_article_crawler import create_guardians_dataset
from tokenization import read_model_and_get_similar_words, print_similarity_table, clean_data_and_create_model

targetwords = ['shocked', 'fake']
# Crawl articles from Guardians website
path = create_guardians_dataset(path='./', articleCount=40000, category='world')
# Creating Word2Vec model
model = clean_data_and_create_model(dataPath=path, modelPath='./MyModel.model')
# Loading model and getting similar words
similarwords, distances = read_model_and_get_similar_words(modelPath='./MyModel.model', numberOfSimilarWords=3,
                                                           targetWords=targetwords)
# Print(similarwords)
print_similarity_table(targetwords, similarwords, distances)
