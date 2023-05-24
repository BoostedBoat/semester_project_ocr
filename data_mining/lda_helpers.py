import pyLDAvis.gensim

import gensim
import gensim.corpora as corpora


stopwords = ['toujours', 'quand', 'souvent', 'leur', 'leurs', 'toute', 'sous', 'n\'est', 'ainsi', 'cela', 'j\'ai', 'alors', 'aussi', 'très', 'entre', 'fait', 'dont', 'non', 'plus', 'c\'est', 'qu\'il', 'cette', 'comme', 'tout', 'tous', 'd\'un', 'd\'une', 'sans', 'faire', 'peut']

def extract_words_from_df(df):
    data_words = []
    for j in range(len(df.index)):
        text = str(df.at[j, 'text'])
        words = text.split(" ")
        words_rm = [i for i in words if i not in stopwords]

        data_words.append(words_rm)
    return data_words

def train_model(data_words, nbr_of_topics, passes):
    # Create dictionary
    id2word = corpora.Dictionary(data_words)

    # Term Document Frequency
    corpus = [id2word.doc2bow(t) for t in data_words]

    print("Training model")
    lda_model = gensim.models.LdaMulticore(corpus=corpus, id2word=id2word, num_topics = nbr_of_topics, passes=passes, iterations=100)

    return lda_model, corpus

def visualize_and_store_lda_model(name, lda_model, corpus):
    vis = pyLDAvis.gensim.prepare(lda_model, corpus, dictionary=lda_model.id2word)
    pyLDAvis.save_html(vis, name)