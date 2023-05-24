import density
import os
import sys
import pandas as pd

in_folder = sys.argv[1]

topic_words = ['freud', 'inconscient', 'rêve', 'ernest jones', 'analytique', 'divan']

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