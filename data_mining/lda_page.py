import pandas as pd
import sys
import os
import lda_helpers
from pprint import pprint

in_folder = sys.argv[1]
nbr_of_topics = sys.argv[2]

passes=1
if len(sys.argv) > 3:
    passes = int(sys.argv[3])

if __name__ == '__main__':
    main_dir = os.listdir(in_folder)
    data_words = []

    for i, node_dir in enumerate(main_dir):
        month_file = os.listdir(in_folder + "/" + node_dir)

        for issue in month_file:
            empty = False
            try:
                df = pd.read_csv(in_folder + "/" + node_dir + "/" + issue, index_col=0)
            except pd.errors.EmptyDataError:
                empty = True
            
            if not empty:
                d = lda_helpers.extract_words_from_df(df)
                for i in d:
                    data_words.append(i)
    
    
    lda_model, corpus = lda_helpers.train_model(data_words, nbr_of_topics, passes)
    pprint(lda_model.print_topics())

    print("Visualizing model")
    lda_helpers.visualize_and_store_lda_model("lda_page_" + str(nbr_of_topics) + "_" + str(passes), lda_model, corpus)