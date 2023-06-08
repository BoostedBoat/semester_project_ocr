## python corpus_to_df.py in_csv in_folder

import df_helpers
import sys
import os
import pandas as pd

def add_entry(df, year, month, text):
    df.at[(year-1970)*12 + month-1,'text'] = text
    return df

in_csv = sys.argv[1]
in_folder = sys.argv[2]

df = pd.read_csv(in_csv, index_col=0)

dir = os.listdir(in_folder)

year = 1970

for t in dir:
    df = df_helpers.add_one_year(df, year, in_folder + "/" + t)
    year += 1

df.to_csv(in_csv)