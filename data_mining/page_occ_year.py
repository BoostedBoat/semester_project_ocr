#python page_occ_year.py in_folder word [distance]

import sys
import os
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


in_folder = sys.argv[1]
word = sys.argv[2]
distance = 0

if len(sys.argv) > 3:
    distance = int(sys.argv[3])

main_dir = os.listdir(in_folder)

occs = np.zeros((len(main_dir)))

for i, node_dir in enumerate(main_dir):
    print(node_dir)
    month_file = os.listdir(in_folder + "/" + node_dir)

    for issue in month_file:
        empty = False
        try:
            df = pd.read_csv(in_folder + "/" + node_dir + "/" + issue, index_col=0)
        except pd.errors.EmptyDataError:
            empty = True
        
        if not empty:
            for j in range(len(df.index)):
                txt = str(df.at[j, 'text'])
                words = txt.split(" ")

                for w in words:
                    if compute_distance(w, word) <= distance:
                        occs[i] += 1
                        break

print(occs)

plt.title("Nbr of pages where " + word + " appears.")
plt.xlabel("Years")
plt.ylabel("Nbr")
plt.bar(np.arange(len(occs)), occs, 0.7)
plt.xticks(np.arange(0, len(occs)), np.arange(1970, 1970 + len(occs)))
plt.show()