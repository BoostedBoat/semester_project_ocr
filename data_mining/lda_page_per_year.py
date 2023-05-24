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
    for i, node_dir in enumerate(main_dir):
        month_file = os.listdir(in_folder + "/" + node_dir)
        print(node_dir)
        data_words = []
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
        
        print(len(data_words))
        if len(data_words) > 0:
            lda_model, corpus = lda_helpers.train_model(data_words, nbr_of_topics, passes)
            pprint(lda_model.print_topics())
            lda_helpers.visualize_and_store_lda_model("lda_"+node_dir+"_"+str(nbr_of_topics)+"_"+str(passes), lda_model, corpus)
    