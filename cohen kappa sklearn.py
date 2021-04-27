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

labels = pd.read_csv('/Users/lidiiamelnyk/Documents/Distribution_ukrainian_comments_khar_puhach_binary.csv', sep = ';', header = 0)

labeler1 = list(labels['Khar is hate'])
labeler2 = list(labels['Puhach is hate'])

cohens = cohen_kappa_score(labeler1, labeler2)
print("Cohens kappa between annotator labeler1 and labeler2: {:.3f}".format(cohens))

matthews_corrcoef_score = matthews_corrcoef(labeler1, labeler2)
print("Matthews corrcoef score between annotator labeler1 and labeler2: {:.3f}".format(matthews_corrcoef_score))

labeler1, labeler2 = make_multilabel_classification(random_state=0)
inner_clf = LogisticRegression(solver="liblinear", random_state=0)
clf = MultiOutputClassifier(inner_clf).fit(labeler1, labeler2)
y_score = np.transpose([y_pred[:, 1] for y_pred in clf.predict_proba(labeler1)])
roc_auc_score_multi = roc_auc_score(labeler2, y_score, average=None)
