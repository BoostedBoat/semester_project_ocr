from PyPDF2 import PdfReader
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk import word_tokenize
import sys
import os
import string

def treat_text(txt):
    entire_text = ""

    for line in txt.split('\n'):
        no_newline = line[:len(line)-1]
        if len(no_newline) > 0:
            no_dash = no_newline
            if (no_newline[-1] == '-'):
                no_dash = no_newline[:len(no_dash)-1]
            else:
                no_dash = no_newline + " "
            entire_text = entire_text + no_dash

    sw = set(stopwords.words('french') + list(string.punctuation))
    entire_text = [i for i in word_tokenize(entire_text.lower()) if i not in sw and len(i) > 2]

    flattened_text = ' '.join(entire_text)

    return flattened_text



in_folder = sys.argv[1]
out_folder_raw = sys.argv[2]
out_folder_treated = sys.argv[3]

dir = os.listdir(in_folder)

for issue in dir:
    print(issue)
    pages = []
    treated_pages = []

    in_file = in_folder + "/" + issue

    reader = PdfReader(in_file)

    for page in reader.pages:
        text_from_page = page.extract_text()
        pages.append(text_from_page)
        treated_pages.append(treat_text(text_from_page))

    raw_dict = {"page": np.arange(1, len(reader.pages)+1), "text": pages}
    treated_dict = {"page": np.arange(1, len(reader.pages)+1), "text": treated_pages}
    
    raw_df = pd.DataFrame(data=raw_dict)
    treated_df = pd.DataFrame(data=treated_dict)

    raw_df.to_csv(out_folder_raw + "/" + "raw_pages_" + issue.split(".")[0] + ".csv")
    treated_df.to_csv(out_folder_treated + "/" + "treated_pages_" + issue.split(".")[0] + ".csv")