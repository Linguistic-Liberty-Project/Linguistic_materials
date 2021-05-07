import pandas as pd
import stanza
stanza.download('uk')
file = pd.read_csv('/Users/lidiiamelnyk/Documents/hatespeech_zn_ua.csv')
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

for i, row in file.iterrows():
	tokenized_sents = []
	for i in row['comment'].split(' '):
		doc = nlp(row['comment'])
		sentenciz = doc.sentences[0].tokens
		for t in sentenciz:
			tokens = {x['text']: x for x in sentenciz}
			tokenized_sents.append(tokens)
	file.at[i,'tokenized'] = ' '.join(tokenized_sents)

