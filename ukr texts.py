import pandas as pd
df = pd.read_csv('/Users/lidiiamelnyk/Downloads/articles_russian.txt', delimiter = "\t")
df = df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)
df.to_csv('/Users/lidiiamelnyk/Downloads/articles_russian_no_duplicates.txt', header=False, index=False, sep='\t', mode='a')