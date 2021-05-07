import pandas as pd
from symspellpy import SymSpell, Verbosity

dataframe1 = pd.read_csv("/Users/lidiiamelnyk/Documents/comments_zn_ua.csv", sep=',',
                         encoding='utf-8-sig',
                         float_precision='round_trip')
ukrainian_dataframe = dataframe1[dataframe1['predicted_language'] == 'Ukrainian']
ukrainian_dataframe = ukrainian_dataframe.drop_duplicates()

sym_spell = SymSpell()
with open("/Users/lidiiamelnyk/Downloads/dss-plugin-nlp-preparation-main/resource/dictionaries/uk.txt", 'r',
          encoding='utf-8-sig') as myfile:
    corpus = myfile.read()
corpus_path = "/Users/lidiiamelnyk/Downloads/dss-plugin-nlp-preparation-main/resource/dictionaries/uk.txt"
symspell_dictionary = sym_spell.load_dictionary(corpus_path, term_index=0, count_index=1, separator=None,
                                                encoding='utf-8-sig')

ukrainian_dataframe['comment'] = ukrainian_dataframe['comment'].astype(str)
ukrainian_dataframe['comments_corrected'] = ukrainian_dataframe['comment'].apply(
    lambda x: (sym_spell.lookup(x, Verbosity.CLOSEST, max_edit_distance=0, include_unknown = True,  transfer_casing=False,ignore_token=r"\w+\d")))

#for i, row in ukrainian_dataframe.iterrows():
 #   if len(row['comments_corrected']) > 0:
  #      pass
   # else:
    #    row['comment'].replace(to_replace=[i for i in row['comment']], value=[i for i in row['comments_corrected']], inplace=False, limit=None,
     #                           regex=False, method='pad')

   # print(ukrainian_dataframe['comment'].head())


with open('/Users/lidiiamelnyk/Documents/zn_ua_ukr_corrected.csv', 'w+', newline = '', encoding='utf-8-sig') as file:
    ukrainian_dataframe.to_csv(file, sep=',', na_rep='', float_format=None,
               columns=['url', 'comment', 'date', 'name','predicted_language'],
               header=True, index=False, index_label=None,
               mode='a', compression='infer',
               quoting=None, quotechar='"', line_terminator=None, chunksize=None,
               date_format=str, doublequote=True, escapechar=None, decimal='.', errors='strict')
    file.close()