from sklearn.dummy import DummyClassifier
from sklearn.svm import SVC
import pandas as pd
y_train_df = pd.read_csv( '/Users/lidiiamelnyk/Documents/russian_comments.csv', sep=';',
                         encoding='utf-8-sig',
                         float_precision='round_trip', header = 0)
y_train = list(y_train_df['Label'])
x_train_df =  pd.read_csv( '/Users/lidiiamelnyk/Documents/russian_comments.csv', sep=';',
                         encoding='utf-8-sig',
                         float_precision='round_trip', header = 0)
x_train = list(x_train_df['Label'])

x_test_df = pd.read_csv('/Users/lidiiamelnyk/Documents/hatespeech_zn_ua.csv', sep=';',
                         encoding='utf-8-sig',
                         float_precision='round_trip', header = 0)
x_test = x_test_df['Label'].astype(float)
y_test_df = pd.read_csv('/Users/lidiiamelnyk/Documents/hatespeech_zn_ru.csv', sep=';',
                         encoding='utf-8-sig',
                         float_precision='round_trip', header = 0)
y_test = y_test_df['Label'].astype(float)

clf = SVC(kernel='linear', C=1).fit(x_train, y_train)
print(clf.score(x_test, y_test))
clf = DummyClassifier(strategy='most_frequent', random_state=0)
clf.fit(x_train, y_train)
clf.score(x_test, y_test)
