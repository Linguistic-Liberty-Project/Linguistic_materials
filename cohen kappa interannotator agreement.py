import pandas as pd

import pandas as pd


def cohen_kappa(ann1, ann2):
    """Computes Cohen kappa for pair-wise annotators.
        :param ann1: annotations provided by first annotator
        :type ann1: list
        :param ann2: annotations provided by second annotator
        :type ann2: list
        :rtype: float
        :return: Cohen kappa statistic
        """
    count = 0
    for an1, an2 in zip(ann1, ann2):
        if an1 == an2:
            count += 1
    A = count / len(ann1)  # observed agreement A (Po)

    uniq = set(ann1 + ann2)
    E = 0  # expected agreement E (Pe)
    for item in uniq:
        cnt1 = ann1.count(item)
        cnt2 = ann2.count(item)
        count = ((cnt1 / len(ann1)) * (cnt2 / len(ann2)))
        E += count

    return round((A - E) / (1 - E), 4)


ann1_pd = pd.read_csv('/Users/lidiiamelnyk/Downloads/Distribution_ukrainian_comments_MARIA_KHAR .csv',sep='delimiter',header =1,  encoding = 'utf-8-sig')
ann2_pd = pd.read_csv('/Users/lidiiamelnyk/Downloads/Distribution_ukrainian_comments_puhach.csv', sep='delimiter', header = 1, encoding = 'utf-8-sig')

ann1 = ann1_pd['HATE/NO'].tolist()
ann2 = ann2_pd['HATE/NO'].tolist()

my_cohen_kappa = cohen_kappa(ann1,ann2)
print(my_cohen_kappa)