import pandas as pd
import stanza
import re
stanza.download('uk')
file = pd.read_csv('/Users/lidiiamelnyk/Documents/hatespeech_zn_ua.csv', index_col=None, sep = ',', header=0,  encoding='utf-8-sig',
                         float_precision='round_trip')
comments_row = file['comment']

config = {
	'processors': 'tokenize,mwt,pos', # Comma-separated list of processors to use
	'lang': 'fr', # Language code for the language to build the Pipeline in
	'tokenize_model_path': './fr_gsd_models/fr_gsd_tokenizer.pt', # Processor-specific arguments are set with keys "{processor_name}_{argument_name}"
	'mwt_model_path': './fr_gsd_models/fr_gsd_mwt_expander.pt',
	'pos_model_path': './fr_gsd_models/fr_gsd_tagger.pt',
	'pos_pretrain_path': './fr_gsd_models/fr_gsd.pretrain.pt',
	'tokenize_pretokenized': True # Use pretokenized text as input and disable tokenization
}

nlp = stanza.Pipeline('uk', processors='tokenize, pos, lemma', tokenize_no_ssplit = True) #create nlp pipeline
myfile = open('/Users/lidiiamelnyk/Documents/stop_words_ua.txt', "r", encoding = 'utf-8-sig') #upload the stopwords
content = myfile.read()
stopwords_list = content.split("\n") #since stopwords come in a form of a list, split them based on the newline


for iter, row in file.iterrows():
	lemmatized_sents = [] #create the list, I am going to append lemmas into
	file['comment'] = file['comment'].astype(str) #change type of data to str as it is required to process the file in the nlp pipeline
	if isinstance(row['comment'],float): #handling the failure where it is for some reason always tpe float
		continue
	doc = nlp(row['comment']) #create the doc file from the nlp pipeline
	sentenciz = doc.sentences[0].tokens #get tokens
	for t in sentenciz:
		pos_tags = t.words[0].pos #for each token get the part of speech tag
		allowed_tags = ['VERB', 'NOUN', 'PROPN', 'ADJ', 'DET', 'ADV'] #create the list of tags I want to sort by
		for tag in pos_tags.split(' '):
			if tag in allowed_tags:
				lemmatized_sents.append(t.words[0].lemma.lower())
		file.at[iter, 'lemmatized'] =  lemmatized_sents



for i, row in file.iterrows():
	stop_words_free_lemmas = []
	for word in row['lemmatized']:
		if word not in stopwords_list:
			stop_words_free_lemmas.append(word)
	file.at[i, 'stop_words_free_lemmas'] = stop_words_free_lemmas

new_columns = ['comment', 'date', 'model_result', 'stop_words_free_lemmas']

file = file.reindex(columns = new_columns)
with open('/Users/lidiiamelnyk/Documents/tokenized_dataframe.csv', 'w+', encoding='utf-8-sig', newline='') as file:
	file.to_csv(file, sep=',', na_rep='', float_format=None, columns = new_columns,
			   header=True, index=False, index_label=None,
			   mode='a', compression='infer',
			   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
			   date_format=None, doublequote=True, escapechar=None, decimal='.')





