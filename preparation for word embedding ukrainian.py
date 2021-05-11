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

nlp = stanza.Pipeline('uk', processors='tokenize, pos', tokenize_no_ssplit = True)

for iter, row in file.iterrows():
	tokenized_sents = []
	file['comment'] = file['comment'].astype(str)
	if isinstance(row['comment'],float):
		continue
	#for i in row['comment'].split(" "):
	doc = nlp(row['comment'])
	sentenciz = doc.sentences[0].tokens
	for t in sentenciz:
		tokenized_sents.append(t.text)
		file.at[iter, 'tokenized'] = tokenized_sents
#pos - t.words[0].pos
sentences = file['tokenized']

sentences = sentences.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
sentences = sentences.map(lambda x: re.sub('[,\.!?]', '', x))  # remove punctuation
sentences = sentences.map(lambda x: x.lower())

myfile = open('/Users/lidiiamelnyk/Documents/stop_words_ua.txt', "r", encoding = 'utf-8-sig')
content = myfile.read()
stopwords_list = content.split(",")

sentences = sentences(lambda x: x for x in sentences if x not in stopwords_list)

with open('/Users/lidiiamelnyk/Documents/tokenized_dataframe.csv', 'w+', encoding='utf-8-sig', newline='') as file:
	sentences.to_csv(file, sep=',', na_rep='', float_format=None,
			   header=True, index=False, index_label=None,
			   mode='a', compression='infer',
			   quoting=None, quotechar='"', line_terminator=None, chunksize=None,
			   date_format=None, doublequote=True, escapechar=None, decimal='.')





