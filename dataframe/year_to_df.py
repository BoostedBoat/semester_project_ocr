#python year_to_df.py in_csv, in_folder, year
#MAKE SURE ALL TXT FILES ARE IN CHRONOLOGICAL ORDER, AND THAT NO MONTH IS MISSING

import sys
import os
import pandas as pd


def add_entry(df, year, month, text):
    df.at[(year-1970)*12 + month-1,'text'] = text

in_csv = sys.argv[1]
in_folder = sys.argv[2]
year = int(sys.argv[3])

df = pd.read_csv(in_csv, index_col=0)

dir = os.listdir(in_folder)

month = 1
for t in dir:
    print(t)
    in_file = in_folder + "/" + t

    print(in_file)
    text = None
    with open(in_file) as file:
        text = file.readlines()

    if len(text) != 0:
        add_entry(df, year, month, text[0])
    month += 1

df.to_csv(in_csv)

