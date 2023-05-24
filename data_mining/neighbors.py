# python neighbors.py in_csv word neighborhood [distance] [top_k]

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from nltk import word_tokenize

def rm_stopwords(txt):
    stopwords = ["plus", "comme", "tout", "cette", "c'est", "fait", "d'un", "qu'il", "n'est", "telle", "peut", "dont", "faire"]

    return [i for i in word_tokenize(txt.lower()) if i not in stopwords]

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

in_csv = sys.argv[1]
word = sys.argv[2]
neighborhood = int(sys.argv[3])

dist = 3
if len(sys.argv) > 4:
    dist = int(sys.argv[4])

top_k = 10
if len(sys.argv) > 5:
    top_k = int(sys.argv[5])

df = pd.read_csv(in_csv, index_col=0)

neighbors = {}

for i in range (len(df.index)):
    if i % 10 == 0:
        print(i)

    text = str(df.at[i, 'text'])

    words = rm_stopwords(text)

    for j, w in enumerate(words):
        if compute_distance(w, word) <= dist:
            for k in range(j-neighborhood, j+neighborhood):
                if k >= 0 and k < len(words):
                    if words[k] in neighbors: 
                        neighbors[words[k]] += 1
                    else:
                        neighbors[words[k]] = 1

sorted_neighbors = dict(reversed(sorted(neighbors.items(), key=lambda x:x[1])))

to_del = []
for elem_key in sorted_neighbors.keys():
    if compute_distance(elem_key, word) <= dist:
        to_del.append(elem_key)

for d in to_del:
    del sorted_neighbors[d]

n_keys = list(sorted_neighbors.keys())[1:top_k+1]
n_vals = list(sorted_neighbors.values())[1:top_k+1]


fig, ax = plt.subplots()

y_pos = np.arange(top_k)

ax.barh(y_pos, n_vals, align='center')
ax.set_yticks(y_pos, labels=n_keys)
ax.invert_yaxis()  # labels read top-to-bottom
ax.set_xlabel('Occurrences')
ax.set_title('Which words appear next to ' + word)

plt.show()
