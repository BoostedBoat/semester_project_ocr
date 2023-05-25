#python create_dataframe.py out_path

import pandas as pd
import numpy as np
import sys

out_path = sys.argv[1]

years = np.zeros((15*12))
months = np.zeros((15*12))
texts = np.empty((15*12), dtype=str)

for y in range(1970, 1985):
    for m in range(12):
        years[(y-1970)*12 + m] = y
        months[(y-1970)*12 + m] = m+1
        texts[(y-1970)*12 + m] = ""

d={
    'year': years,
    'month': months,
    'text': texts
}

df = pd.DataFrame.from_dict(d)

df.to_csv(out_path)