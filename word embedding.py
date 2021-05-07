import pandas as pd
import stanza
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

nlp = stanza.Pipeline('uk', processors='tokenize', tokenize_no_ssplit = True)

for iter, row in file.iterrows():
	tokenized_sents = []
	file['comment'] = file['comment'].astype(str)
	if isinstance(row['comment'],float):
		continue
	for i in row['comment'].split(" "):
		doc = nlp(row['comment'])
		sentenciz = doc.sentences[0].tokens
		for t in sentenciz:
			for j in t.words:
				tokenized_sents.append(j.text)
	file.at[iter,'tokenized'] = ' '.join(tokenized_sents)

print(file.head())

