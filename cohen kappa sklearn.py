from sklearn.metrics import cohen_kappa_score
from sklearn import metrics
import pandas as pd
import numpy as np

labels = pd.read_csv('/Users/lidiiamelnyk/Documents/Distribution_ukrainian_comments_khar_puhach_binary.csv', sep = ';', header = 0)

labeler1 = list(labels['Khar is hate'])
labeler2 = list(labels['Puhach is hate'])

cohens = cohen_kappa_score(labeler1, labeler2)
print("Cohens kappa between annotator labeler1 and labeler2: {:.3f}".format(cohens))
from sklearn.metrics import matthews_corrcoef
print(matthews_corrcoef(labeler1, labeler2))
