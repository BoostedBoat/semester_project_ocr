#python txt_to_df.py in_csv, year, month, in_text

import sys
import pandas as pd

in_csv = sys.argv[1]
year = int(sys.argv[2])
month = int(sys.argv[3])
in_text = sys.argv[4]

def add_entry(df, year, month, text):
    df.at[(year-1970)*12 + month-1,'text'] = text

df = pd.read_csv(in_csv, index_col=0)

text = None
with open(in_text) as file:
    text = file.readlines()

add_entry(df, year, month, text)

df.to_csv(in_csv)

