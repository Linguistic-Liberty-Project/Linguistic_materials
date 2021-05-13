import pandas as pd
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
from gensim.models.phrases import Phrases, Phraser
import numpy as np
import itertools
from time import time  # To time our operations
from collections import defaultdict  # For word frequency
import multiprocessing

import logging  # Setting up the loggings to monitor gensim
logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)

file = pd.read_csv('/Users/lidiiamelnyk/Documents/lemmatized_dataframe.csv',  sep = ',', encoding='utf-8-sig',
                         float_precision='round_trip')

#sent = file['lemmatized'].astype(str)
import re
for iter, row in file.iterrows():
    sent = []
    file['lemmatized'] = file['lemmatized'].astype(str)
    if isinstance(row['lemmatized'], float):  # handling the failure where it is for some reason always tpe float
        continue
    for word in row['lemmatized'].split(' '):
        words = re.findall('\w+', word)
        words = " ".join(words)
        sent.append(words)
    file.at[iter, 'changed'] =" ,".join(sent)


sent1 =  [row.split() for row in file['changed'].astype(str)]

phrases = Phrases(sent1, min_count=20, progress_per=10000)

bigram = Phraser(phrases)

sentences = bigram[sent1]
#carry out the word frequency calculations as a sanity check of the effectiveness of the lemmatization, removal of stopwords, and addition of bigrams.

word_freq = defaultdict(int)
for sent in sentences:
    for i in sent:
        word_freq[i] += 1 #basically calculate each new word
print(len(word_freq))

#3 steps of building the model: In this first step, I set up the parameters of the model one-by-one.
# Here it builds the vocabulary from a sequence of sentences and thus initialized the model.
#train the model

cores = multiprocessing.cpu_count() # Count the number of cores in a computer
w2v_model = Word2Vec( min_count=10, #the words (bigrams) should be met in a corpus at least this number of times
                     window=3,  #The maximum distance between the current and predicted word within a sentence. E.g. window words on the left and window words on the left of our target
                     sample=6e-5, #float - The threshold for configuring which higher-frequency words are randomly downsampled. Highly influencial.
                     alpha=0.07, #The initial learning rate
                     min_alpha=0.0007, # Learning rate will linearly drop to min_alpha as training progresses.
                     negative=15, #negative sampling will be used, the int for negative specifies how many "noise words" should be drown.
                     workers=cores-1) #Use these many worker threads to train the model (=faster training with multicore machines
t = time()

w2v_model.build_vocab(sentences, progress_per=10000)

print('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))

w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=50, report_delay=1) #total examples is count of sentences, epochs is number of iterations over a corpus

print('Time to train the model: {} mins'.format(round((time() - t) / 60, 2)))

print(w2v_model.wv.most_similar(positive=["вакцина"]))