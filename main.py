import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix, classification_report


def file2sentences(filename):
    txt = ""
    with open(filename, "r", encoding="utf-8") as f:
        txt = f.read()

        txt = txt.replace("?", ".")
        txt = txt.replace("!", ".")
        txt = txt.replace("»", "")
        txt = txt.replace("«", "")
        txt = txt.replace(":", "")
        txt = txt.replace(";", "")
        txt = txt.replace("...", ".")
        txt = txt.replace("…", ".")
        txt = txt.replace("\n", ".")
        txt = txt.replace("  ", " ")
        txt = txt.replace("\"", "")
        txt = txt.replace("„", "")

        sentences = txt.split(".")
        for i in range(len(sentences)):
            sentences[i] = sentences[i].strip()

        sentences = [x for x in sentences if x != ""]
        return sentences


ukrainian = file2sentences("/Users/lidiiamelnyk/Downloads/articles_no_duplicates.txt")
russian = file2sentences("/Users/lidiiamelnyk/Downloads/articles_russian_no_duplicates.txt")
#surzhyk = file2sentences("/Users/lidiiamelnyk/Downloads/surzhyk.txt")

X = np.array(ukrainian + russian)
y = np.array(['uk'] * len(ukrainian) + ['ru'] * len(russian))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

cnt = CountVectorizer(analyzer='char', ngram_range=(2, 2))

pipeline = Pipeline([('vectorizer', cnt), ('model', MultinomialNB())])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))


dataframe1 = pd.read_csv("/Users/lidiiamelnyk/Downloads/comments_new_test_23_100.csv", sep=',', encoding='utf-8-sig',
                         float_precision='round_trip')


spec_chars = ['"',"#","%","&","'","(",")",
              "*","+","/",";","<",
              "=",">","?","@","[","\\","]","^","_",
              "`","{","|","}","~","–", '$']
for char in spec_chars:
    dataframe1['comments'] = dataframe1['comments'].str.replace(char, ' ')

print (dataframe1['comments'].head())

for i, row in dataframe1.iterrows():
    language = []
    dataframe1['comments'] = dataframe1['comments'].astype(str)
    for line in row['comments'].split(" "):
        line = [line]
        language_pred = pipeline.predict(line)
        language.append(str(language_pred))
    dataframe1.at[i, 'detected_language_array'] = ' '.join(language)

import math

for i, row in dataframe1.iterrows():
    dataframe1['detected_language_array'] = dataframe1['detected_language_array'].astype(str)
    array_from_string = row['detected_language_array'].split(' ')
    all_l2w_count = len(array_from_string)
    ukr_words = row['detected_language_array'].count("['uk']")
    ru_words = row['detected_language_array'].count("['ru']")
    #szk_words = row['detected_language_array'].count("['szh']")
    percentage_ukr = math.ceil((ukr_words / all_l2w_count) * 100) / 100
    percentage_ru = math.ceil((ru_words / all_l2w_count) * 100) / 100
    #percentage_szk = math.ceil((szk_words / all_l2w_count) * 100) / 100
    if percentage_ukr > 0.70:
        dataframe1.at[i, 'predicted_language'] = "Ukrainian"
    elif percentage_ru > 0.70:
        dataframe1.at[i, 'predicted_language'] = "Russian"
    else:
        dataframe1.at[i, 'predicted_language'] = "Surzhyk"

dataframe1 = dataframe1.reindex(columns = ['url', 'comments','date','predicted_language'])

with open('/Users/lidiiamelnyk/Downloads/comments_test_23_100_with_language_70_pr.csv', 'w+', newline = '', encoding='utf-8-sig') as file:
    dataframe1.to_csv(file, sep=',', na_rep='', float_format=None,
               columns=['url', 'comments', 'date', 'predicted_language'],
               header=True, index=False, index_label=None,
               mode='a', compression='infer',
               quoting=None, quotechar='"', line_terminator=None, chunksize=None,
               date_format=None, doublequote=True, escapechar=None, decimal='.', errors='strict')
    file.close()