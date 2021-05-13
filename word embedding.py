import pandas as pd
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
from gensim.models.phrases import Phrases, Phraser
import numpy as np
import itertools
from time import time  # To time our operations
from collections import defaultdict  # For word frequency

import spacy  # For preprocessing

import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

file = pd.read_csv('/Users/lidiiamelnyk/Documents/tokenized_dataframe.csv',  sep = ',', encoding='utf-8-sig',
                         float_precision='round_trip')

sent = file['stop_words_free_lemmas']
phrases = Phrases(sent, min_count=30, progress_per=10000)
bigram = Phraser(phrases)

sentences = bigram[sent] #transform corpus based on bigrams detected

#carry out the word frequency calculations as a sanity check of the effectiveness of the lemmatization, removal of stopwords, and addition of bigrams.