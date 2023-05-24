import pandas as pd
import sys
import gensim
import gensim.corpora as corpora
from pprint import pprint

to_remove = ['plus', 'c\'est', 'qu\'il', 'cette', 'comme', 'tout', 'tous', 'd\'un', 'd\'une', 'sans', 'faire', 'peut']

in_csv = sys.argv[1]
nbr_of_topics = sys.argv[2]

passes=1
if len(sys.argv) > 3:
    passes = int(sys.argv[3])

df = pd.read_csv(in_csv, index_col=0)

def get_data(year):

    data_words = []

    for i in range(len(df.index)):
        if df.at[i, 'year'] == year:
            text = str(df.at[i, 'text'])
            words = text.split(" ")
            words_rm = [i for i in words if i not in to_remove]

            data_words.append(words_rm)
    
    return data_words

if __name__ == '__main__':
    models = []

    years = df[['year']].drop_duplicates()

    for k in years.index:
        i = years.at[k, 'year']
        data_words = get_data(i)

        if len(data_words) != 0:
            # Create dictionary
            id2word = corpora.Dictionary(data_words)

            # Term Document Frequency
            corpus = [id2word.doc2bow(t) for t in data_words]

            print("Training model for year " + str(i))
            lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=id2word, num_topics = nbr_of_topics, passes=passes, iterations=100)

            models.append(lda_model)
        else:
            models.append(None)

    for i, j in enumerate(models):
        print("\nModel year " + str(years.index[i]))
        if j == None:
            print("No data for this year")
        else:
            pprint(j.print_topics())