# python density_entire_corpus.py in_folder topic_words

import density
import os
import sys
import pandas as pd
import csv

in_folder = sys.argv[1]
#csv, one word per row
topic_words_csv = sys.argv[2]

import csv

topic_words = []

with open(topic_words_csv, 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    topic_words.append(row[0])

main_dir = os.listdir(in_folder)

for i, node_dir in enumerate(main_dir):

    month_file = os.listdir(in_folder + "/" + node_dir)

    for issue in month_file:
        print("Issue " + issue)

        #manage missing issues
        empty = False
        try:
            df = pd.read_csv(in_folder + "/" + node_dir + "/" + issue, index_col=0)
        except pd.errors.EmptyDataError:
            empty = True
            print("Missing issue")

        if not empty:
            density.get_interesting_articles(df, topic_words)
        print("")