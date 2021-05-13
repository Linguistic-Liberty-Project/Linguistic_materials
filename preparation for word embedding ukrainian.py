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

nlp = stanza.Pipeline('uk', processors='tokenize, pos, lemma', tokenize_no_ssplit = True)
myfile = open('/Users/lidiiamelnyk/Documents/stop_words_ua.txt', "r", encoding = 'utf-8-sig')
content = myfile.read()
stopwords_list = content.split("\n")


for iter, row in file.iterrows():
	tokenized_sents = []
	lemmatized_sents = []
	file['comment'] = file['comment'].astype(str)
	if isinstance(row['comment'],float):
		continue
	#for i in row['comment'].split(" "):
	doc = nlp(row['comment'])
	sentenciz = doc.sentences[0].tokens
	for t in sentenciz:
		#tokenized_sents.append(t.text)
		pos_tags = t.words[0].pos
		allowed_tags = ['VERB', 'NOUN', 'PROPN', 'ADJ', 'DET', 'ADV']
		for tag in pos_tags.split(' '):
			if tag in allowed_tags:
				#lemmas = t.words[0].lemma.lower()
				#for lemma in lemmas.split(' '):
					#if len(lemma)>3:
				lemmatized_sents.append(t.words[0].lemma.lower())
		#file.at[iter, 'tokenized'] = tokenized_sents
		file.at[iter, 'lemmatized'] =  lemmatized_sents
#pos - t.words[0].pos



for i, row in file.iterrows():
	stop_words_free_lemmas = []
	for word in row['lemmatized']:
		if word in stopwords_list:
			pass
		else:
			stop_words_free_lemmas.append(word)
	file.at[i, 'stop_word_free_lemmas'] = stop_words_free_lemmas

#sentences = sentences(lambda x: x for x in sentences if x not in stopwords_list)

with open('/Users/lidiiamelnyk/Documents/tokenized_dataframe.csv', 'w+', encoding='utf-8-sig', newline='') as file:
	file.to_csv(file, sep=',', na_rep='', float_format=None,
			   header=True, index=False, index_label=None,
			   mode='a', compression='infer',
			   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
			   date_format=None, doublequote=True, escapechar=None, decimal='.')





