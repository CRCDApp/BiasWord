import re

from gensim.models import Word2Vec
from gensim.models.phrases import Phraser, Phrases
from scipy.spatial.distance import cosine
from tabulate import tabulate


def read_data(path):
    """Reading Dataset from specified path

    Parameters:
    path: path of the dataset to open

    Returns:
    opened Dataset
   """

    f = open(path, 'r')
    data = f.read()
    f.close()
    return data


def clean_data(data):
    """ Cleaning input dataset,
        Removing punctuation marks,
        Removing Guardians advertisement setences
        Lowercasing the data

    Parameters:
    data (list): input Dataset

    Returns:
    Cleaned Dataset
   """
    clear_data = []
    # removing punctuations and empty lines
    clear_data = [re.sub(pattern=r'[\!"#$%&\*+,-./:;<=>?@^_`()|~=•–]',
                        repl='',
                        string=x
                        ).strip().split(' ') for x in data.split('\n')
                 if not x.endswith('www.theguardian.com')]
    # removing special carachters and lowercasing the string
    return [[y.replace('“', '').replace('”', '').replace('\'','').lower() for y in x] for x in clear_data if x != ['']]


def detect_bigrams(data):
    """ Detecting Bigrams in input data
        Uses some commong
    Parameters:
    data (list): input Dataset

    Returns:
    Dataset including bigrams
   """
    common_terms = ['of', 'with', 'without', 'and', 'or', 'the', 'a']
    phrases = Phrases(data, common_terms=common_terms)
    bigram = Phraser(phrases)
    return list(bigram[data])


# creating model
def create_w2v_model(data, output='./newGuardiansModel.model', min_count=3, size=200, workers=2, window=5, iter=30):
    """ Creating and saving Word2Vec model

    Parameters:
    data (list): Input Dataset
    min_count (int): Ignore words that appear less than this
    size (int): Dimensionality of word embeddings
    workers (int): Number of processors (parallelisation)
    window (int): Context window for words during training
    iter (int): Number of epochs training over corpus

    Returns:
    Created Word2Vec Model
   """
    model = Word2Vec(data,
                     min_count=min_count,  # Ignore words that appear less than this
                     size=size,  # Dimensionality of word embeddings
                     workers=workers,  # Number of processors (parallelisation)
                     window=window,  # Context window for words during training
                     iter=iter)  # Number of epochs training over corpus
    model.save(output)
    return model


# get most similar words
def getSimilarWords(model, word='shocked', size=100):
    """ Getting SimilarWords according to the model

    Parameters:
    Model: Word2Vec Model
    word: Target word
    size: Number of similar words

    Returns:
    List of similar words
   """
    # get most similar words from trained data ?!
    # return [i[0] for i in model.wv.most_similar(word)[:size]]
    return [i[0] for i in model.most_similar(word, topn=size)]


def clean_data_and_create_model(dataPath='./Guardians-world_207_Articles_2019-11-02_13_10.txt',
                            modelPath='./newGuardiansModels.model', min_count=3, size=200, workers=2, window=5,
                            iter=30):
    """ Cleaning dataset, creating and saving Word2Vec model

    Parameters:
    ModelPath: Path to save output Word2Vec Model
    dataPath: Path to read input Data
    min_count (int): Ignore words that appear less than this
    size (int): Dimensionality of word embeddings
    workers (int): Number of processors (parallelisation)
    window (int): Context window for words during training
    iter (int): Number of epochs training over corpus

    Returns:
    Created Word2Vec Model
   """
    data = read_data(dataPath)
    data = clean_data(data)
    data = detect_bigrams(data)
    return create_w2v_model(data, output=modelPath, min_count=min_count, size=size, workers=workers, window=window,
                          iter=iter)


def read_model_and_get_similar_words(modelPath='./newGuardiansModels.model', targetWords=['shocked', 'fake'],
                                numberOfSimilarWords=20):
    """ Reading input Model and calculating similar words and respective distances

    Parameters:
    ModelPath: Path to load input Word2Vec Model
    targetWords: Target words to find similar words
    size: Number of similar words

    Returns:
    List of similar words
    List of respective Cosine Distance of the similar words
   """
    model = Word2Vec.load(modelPath)
    similar_words = [getSimilarWords(model, word=word, size=numberOfSimilarWords) for word in targetWords]
    distances = [[cosine(model.wv[targetWords[i]], model.wv[sw]) for sw in similar_words[i]] for i in
                 range(len(targetWords))]
    '''
    #dictionary
    #distances_dic = {targetwords[i]:[cosine(model.wv[targetwords[i]],model.wv[similarword]) for similarword in an[i]] for i in range(len(targetwords))}
    
    #model.similarity also returns cosine distance :D
    #dddd = [[model.similarity(targetwords[i],similarword) for similarword in an[i]] for i in range(len(targetwords))]
    '''
    return similar_words, distances


def print_similarity_table(targetwords, similarwords, distances):
    for j in range(len(targetwords)):
        print('\n\nSimilar Words to the Word:\t\"%s\"' % targetwords[j])
        print(tabulate([[similarwords[j][i], distances[j][i]] for i in range(len(similarwords[j]))],
                       headers=['Word', 'Cosine Distance'], tablefmt='fancy_grid'))
