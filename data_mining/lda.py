import pandas as pd
import sys
import gensim
import gensim.corpora as corpora
from pprint import pprint

to_remove = ['plus', 'c\'est', 'qu\'il', 'cette', 'comme', 'tout', 'tous', 'd\'un', 'd\'une', 'sans', 'faire', 'peut']

in_csv = sys.argv[1]
nbr_of_topics = sys.argv[2]

df = pd.read_csv(in_csv, index_col=0)

data_words = []

for i in range(len(df.index)):
    text = str(df.at[i, 'text'])
    words = text.split(" ")
    words_rm = [i for i in words if i not in to_remove]

    data_words.append(words_rm)

if __name__ == '__main__':
    # Create dictionary
    id2word = corpora.Dictionary(data_words)

    # Term Document Frequency
    corpus = [id2word.doc2bow(t) for t in data_words]
    print("Training model")
    lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=id2word, num_topics = nbr_of_topics, passes=10)

    pprint(lda_model.print_topics())
    doc_lda = lda_model[corpus]

    pprint(doc_lda)

