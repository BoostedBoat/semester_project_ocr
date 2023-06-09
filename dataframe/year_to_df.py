#python year_to_df.py in_csv in_folder year
#MAKE SURE ALL TXT FILES ARE IN CHRONOLOGICAL ORDER, AND THAT NO MONTH IS MISSING

import sys
import pandas as pd
import df_helpers

in_csv = sys.argv[1]
in_folder = sys.argv[2]
year = int(sys.argv[3])

df = pd.read_csv(in_csv, index_col=0)

df = df_helpers.add_one_year(df, year, in_folder)

df.to_csv(in_csv)

