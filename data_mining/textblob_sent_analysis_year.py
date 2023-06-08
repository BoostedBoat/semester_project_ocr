#python textblob_sent_analysis_year.py in_csv word neighborhood [dist]


import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
from nltk import word_tokenize

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

def get_sentences(text, word, half_size, dist):
    sentences = []

    words = word_tokenize(text)

    for j, w in enumerate(words):
        if compute_distance(w, word) <= dist:
            beginning = max(0, j-half_size)
            end = min(len(words), j+half_size)
            sentences.append(words[beginning:end])

    return sentences

in_csv = sys.argv[1]
word = sys.argv[2]
half_size = int(sys.argv[3])

dist = 2
if len(sys.argv) > 4:
    dist = int(sys.argv[4])

df = pd.read_csv(in_csv, index_col=0)

mean_year_polarity = []
mean_month_polarity = []

for i in range (len(df.index)):
    if i % 10 == 0:
        print(i)

    polarity = []

    text = str(df.at[i, 'text'])

    sentences = get_sentences(text, word, half_size, dist)

    if len(sentences) > 0:
        for elem in sentences:
            s = ' '.join(elem)
            analysis = TextBlob(s, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[0]
            if analysis < -0.3 or analysis > 0.3:
                polarity.append(TextBlob(s, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[0])

    if len(polarity) > 0:
        mean_month_polarity.append(np.mean(polarity))
    else:
        mean_month_polarity.append(0)

for j in range(0,len(mean_month_polarity), 12):
    mean_year_polarity.append(np.mean(mean_month_polarity[j:j+12]))

plt.title("Polarity of " + word)
plt.xlabel("Months")
plt.ylabel("Polarity")
plt.plot(np.arange(len(mean_year_polarity)), mean_year_polarity)
plt.xticks(np.arange(0, len(mean_year_polarity)), np.arange(1970, 1970 + len(mean_year_polarity)))
plt.show()