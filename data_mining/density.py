import pandas as pd

'''in_issue = sys.argv[1]

topic_words_1 = ['freud', 'inconscient', 'rêve', 'ernest jones', 'analytique', 'divan']
topic_words_2 = ['ellenberger', 'janet', 'jung', 'rogers', 'esalen', 'etats-unis', 'janov']
topic_words_3 = ['cri primal', 'psychodrame', 'gestalt', 'feldenkrais', 'yoga', 'transactionnelle', 'coaching', 'astrologie', 'caractérologie', 'homéopathie', 'gauquelin']
topic_words_4 = ['cognitive', 'comportementale', 'pavlov', 'skinner', 'bandura', 'ellis', 'eysenck', 'wolpe', 'beck']

empty = False
try:
    df = pd.read_csv(in_issue, index_col=0)
except pd.errors.EmptyDataError:
    df = None'''

def create_distance(word):
    return int(len(word)/3)

def compute_distance(word_1, word_2):
    N, M = len(word_1), len(word_2)

    dp = [[0 for i in range(M + 1)] for j in range(N + 1)]

    # Base Case: When N = 0
    for j in range(M + 1):
        dp[0][j] = j
    # Base Case: When M = 0
    for i in range(N + 1):
        dp[i][0] = i
    # Transitions
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            if word_1[i - 1] == word_2[j - 1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(
                    dp[i-1][j], # Insertion
                    dp[i][j-1], # Deletion
                    dp[i-1][j-1] # Replacement
                )

    return dp[N][M]

def extract_words_from_df(df):
    data_words = []
    for j in range(len(df.index)):
        text = str(df.at[j, 'text'])
        words = text.split(" ")

        data_words.append(words)
    return data_words

def get_occurences(df, topic_words):
    word_nbrs = {}
    for w in topic_words:
        word_nbrs[w] = {}

    if df is not None:
        d = extract_words_from_df(df)
        for i, page in enumerate(d):
            for t in topic_words:
                word_nbrs[t][i+1] = 0
                real_t = t.split(' ')
                if len(real_t) == 1:
                    word_nbrs[t][i+1] = sum(map(lambda x : compute_distance(t, x) <= create_distance(t), page))
                else:
                    for page_word in page:
                        found = True
                        for topic_word_split in real_t:
                            if compute_distance(page_word, topic_word_split) > create_distance(topic_word_split) + 1:
                                found = False
                                break
                        if found:
                            word_nbrs[t][i+1] += 1
        return word_nbrs
    else:
        print("Empty dataframe")

def get_global_occurrences(df, word_nbrs):
    total_occs = {}
    for i in range(len(df.index)):
        total_occs[i+1] = 0
        for w in word_nbrs:
            total_occs[i+1] += word_nbrs[w][i+1]
    return total_occs

def get_interesting_pages(total_occurences, threshold=10):
    interesting_pages = []
    interesting_article = []
    last_i = 0
    for i in total_occurences:
        if total_occurences[i] > threshold:
            if last_i != 0 and i - last_i > 2:
                interesting_pages.append(interesting_article)
                interesting_article = []
            
            interesting_article.append(i)
            last_i = i
    if len(interesting_article) != 0:
        interesting_pages.append(interesting_article)
    return interesting_pages

def print_interesting_articles(interesting_pages, word_numbers):
    if len(interesting_pages) == 0:
        print("Aucun article trouvé")
        return
    
    for article in interesting_pages:
        if len(article) == 1:
            print("Page %d:" % article[0])
        else:
            print("Pages %d à %d:" % (article[0], article[-1]))
        total_topic_occ = 0
        for topic_word in word_numbers.keys():
            apparitions = 0
            for i in range(article[0], article[-1]+1):
                apparitions += word_numbers[topic_word][i]
            if apparitions != 0:
                print("Le mot " + topic_word + " apparait %d fois." % apparitions)
            total_topic_occ += apparitions
        print("Au total, %d mots liés au thème ont été trouvés." % total_topic_occ)
        print("")


def get_interesting_articles(df, topic_words):
    word_nbrs = get_occurences(df, topic_words)
    total_occs = get_global_occurrences(df, word_nbrs)
    interesting_pages = get_interesting_pages(total_occs)
    print_interesting_articles(interesting_pages, word_nbrs)