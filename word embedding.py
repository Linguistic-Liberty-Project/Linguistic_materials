import pandas as pd
from gensim.models import Word2Vec
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
from gensim.models import Phrases
import numpy as np
import itertools

file = pd.read_csv('/Users/lidiiamelnyk/Documents/tokenized_dataframe.csv',  sep = ',', encoding='utf-8-sig',
                         float_precision='round_trip')


myfile = open('/Users/lidiiamelnyk/Documents/stop_words_ua.txt', "r", encoding = 'utf-8-sig')
content = myfile.read()
stopwords_list = content.split("\n")

file['tokenized'] = file['tokenized'].map(lambda x: x.lower())
file['shortened'] = file['tokenized'].map(lambda x: len(x)>3)