#python occurrences_year.py in_csv word [distance] [deviation]

import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
distance = 0
deviation = 3

if len(sys.argv) > 3:
    distance = int(sys.argv[3])

if len(sys.argv) > 4:
    deviation = int(sys.argv[4])

df = pd.read_csv(in_csv, index_col=0)

len_occ = int(len(df.index) / 12) + 1

if len(df.index)%12 == 0:
    len_occ -= 1

occ = np.zeros((len_occ))

for i in range (len(df.index)):
    if i%10 == 0:
        print(i)
    text = str(df.at[i, 'text'])

    words = text.split(" ")

    counter = 0
    for w in words:
        if compute_distance(w, word) <= distance:
            counter += 1

    occ[int(i/12)] += counter


colors = ["c"] * int(len(occ))

mean_occ = np.mean(occ)

higher_than_dev = np.argmax(occ)

colors[higher_than_dev] = "red"

print(occ)

plt.title("Occurrences of " + word)
plt.xlabel("Years")
plt.ylabel("Occurrences")
plt.bar(np.arange(len(occ)), occ, 0.7, color=colors)
plt.xticks(np.arange(len(occ)), np.arange(1970, 1970 + len(occ)))
plt.show()