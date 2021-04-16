import pandas as pd
from symspellpy import SymSpell, Verbosity

dataframe1 = pd.read_csv("/Users/lidiiamelnyk/Downloads/comments_test_23_100_with_language_70_pr.csv", sep=',',
                         encoding='utf-8-sig',
                         float_precision='round_trip')
russian_dataframe = dataframe1[dataframe1['predicted_language'] == 'Russian']

sym_spell = SymSpell()

corpus_path = "/Users/lidiiamelnyk/Downloads/dss-plugin-nlp-preparation-main/resource/dictionaries/ru.txt"
symspell_dictionary = sym_spell.load_dictionary(corpus_path, term_index=0, count_index=1, separator=None,
                                                encoding='utf-8-sig')

russian_dataframe['comments'] = russian_dataframe['comments'].astype(str)
russian_dataframe['comments_corrected'] = russian_dataframe['comments'].apply(
    lambda x: (sym_spell.lookup(x, Verbosity.CLOSEST, max_edit_distance=0, include_unknown = True,  transfer_casing=False,ignore_token=r"\w+\d")))

for i, row in russian_dataframe.iterrows():
    if len(row['comments_corrected']) > 0:
        pass
    else:
        row['comments'].replace(to_replace=i, value=[i for i in row['comments_corrected']], inplace=False, limit=None,
                                regex=False, method='pad')

print(russian_dataframe['comments'].head())