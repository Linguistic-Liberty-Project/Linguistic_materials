from sklearn.metrics import cohen_kappa_score
from sklearn import metrics
import pandas as pd
import numpy as np
from sklearn.datasets import make_multilabel_classification
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import explained_variance_score

labels_ua = pd.read_csv('/Users/lidiiamelnyk/Documents/Distribution_ukrainian_comments_khar_puhach_binary.csv', sep = ';', header = 0)
labels_ru = pd.read_csv('/Users/lidiiamelnyk/Documents/Puhach_Khar/Puhach, Khar_binary.csv', sep = ';', header = 0)
labeler1 = list(labels_ua['Khar is hate'])
labeler2 = list(labels_ua['Puhach is hate'])

labeler3 = list(labels_ru['Puhach is 1'])
labeler4 = list(labels_ru['Khar is 1'])
cohens_ua = cohen_kappa_score(labeler1, labeler2)
cohens_ru = cohen_kappa_score(labeler3, labeler4)
type_of_hate_1 = list(labels_ru['Type of HS'])
type_of_hate_2 = list(labels_ru['Type of 1 char'])

print("Cohens kappa for ukrainian comments between annotator labeler1 and labeler2: {:.3f}".format(cohens_ua))
print("Cohens kappa for russian comments between annotator labeler3 and labeler4: {:.3f}".format(cohens_ru))

matthews_corrcoef_score_ua = matthews_corrcoef(labeler1, labeler2)
matthews_corrcoef_score_ru = matthews_corrcoef(labeler3, labeler4)
print("Matthews corrcoef score for ukrainian comments between annotator labeler1 and labeler2: {:.3f}".format(matthews_corrcoef_score_ua))
print("Matthews corrcoef score for russian comments between annotator labeler3 and labeler4: {:.3f}".format(matthews_corrcoef_score_ru))

from nltk.metrics import agreement


# Reformat the data into the form AnnotationTask
#  expects.
labels_ru = labels_ru.dropna( subset = ['Type of HS'])
data = []
for idx, row in labels_ru.iterrows():
    data.append(("a1", idx, row["Type of HS"]))
    data.append(("a2", idx, row["Type of 1 char"]))

atask = agreement.AnnotationTask(data=data)

print("Cohen's Kappa:", atask.kappa())
print("Fleiss's Kappa:", atask.multi_kappa())

