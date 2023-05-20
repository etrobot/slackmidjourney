import ast
import json
import os

import pandas

path='../content/posts/'
filelist=os.listdir(path)
df = pandas.read_csv('midjourney.csv')
df.drop_duplicates('prompt',keep='last',inplace=True)
df.set_index('prompt',inplace=True)
for filename in filelist:
    if not filename.endswith('.md'):
        continue
    with open(path + filename, 'r') as f:
        data = f.read()
        new_data=data
        for k,v in df.iterrows():
            if k in data:
                print(k,df.at[k, 'url'])
                new_data = data.replace(k, df.at[k, 'url'])
    with open(path + filename, 'w') as f:
        f.write(new_data)