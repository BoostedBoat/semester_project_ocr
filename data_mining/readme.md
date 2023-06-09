# data_mining

This folder contains useful scripts for data mining. It also contains a dataframe that can be used by the pandas library, "df_treated.csv", in which entries are composed of a year, a month, and a text (the one of the corresponding magazine), and a folder "pages_treated_txts", which contains one subfolder per year of the magazine, in which we can found a dataframe that can be used by pandas for each issue, each of these containing entries with a page number and the associated text.

## density.py
This script contains helper functions for the density_entire_corpus.py one. It can be used in standalone, as explained in the comments of the file.

## density_entire_corpus.py
This script detects magazines and pages in these magazines that are related to a certain topic. It can help bring out articles talking about a certain topic.
```
python density_entire_corpus.py in_folder topic_words
```
where:
- in_folder is the path to a folder where the "pages_treated_txts" folder, or a similar folder.
- topic_words is the path to a csv containing words (one per row!) related to the topic we want to find related articles for. An example is available in this folder: "topic_words.csv".
Pay attention: this tool is not perfect, it finds the number of topic words in different pages and outputs the ones in which the density is the highest, but the density measure is arbitrary, which means that the outputted pages can differ depending on the given topic words. For it to work, there should be enough specific topic words, and too generic topic words should be avoided.

## lda.py
This script performs lda on a pandas dataframe, in the "text" column (there should be a "text" column in the dataframe). It should only be used in specific situations, are generalization tools are also here available.
```
python lda.py in_csv nbr_of_topics
```
where:
- in_csv is the path to the pandas dataframe
- nbr_of_topics is the number of topics that the lda will focus on.
Pay attention: the topics will only be printed in the terminal at the end of the lda, and not stored anywhere.

## lda_helpers.py
This file contains useful helper functions for the scripts performing lda.

## lda_page.py
This script will execute the lda algorithm on the whole corpus, considering each page as a document. The "pages_treated_txts" folder, or a similar one, should be used as argument. The result will be stored as a html file.
```
python lda_page.py in_folder nbr_of_topics [nbr_of_passes]
```
where:
- in_folder is the path to the "pages_treated_txts" folder, or a similar one
- nbr_of_topics it the number of topics defined for the lda
- [nbr_of_passes] is the number of passes defined for the lda (default is 1)

## lda_page_per_year.py
This script will execute the lda algorithm for each different year, considering each page as a document. The "pages_treated_txts" folder, or a similar one, should be used as argument. The results will be stored as html files.
```
python lda_page_per_year.py in_folder nbr_of_topics [nbr_of_passes]
```
where:
- in_folder is the path to the "pages_treated_txts" folder, or a similar one
- nbr_of_topics it the number of topics defined for the lda
- [nbr_of_passes] is the number of passes defined for the lda (default is 1)

## lda_per_year.py
This script performs lda on "df_treated.csv", or on a similar pandas dataframe. It outputs a list of topic for each year, each time using the whole text of the year as a single document. The results will only be printed, and not stored.
```
python lda_per_year.py in_csv nbr_of_topics [nbr_of_passes]
```
where:
- in_csv is the path to the "df_treated.csv" dataframe, or a similar one
- nbr_of_topics it the number of topics defined for the lda
- [nbr_of_passes] is the number of passes defined for the lda (default is 1)

## mean_page_per_year.py
This script computes the mean page at which a word appears in each magazine, and outputs a mean page for each year.
``` 
python mean_page_per_year.py in_folder word [distance]
```
where:
- in_folder is the "pages_treated_txts" folder, or a similar one
- word is the word we're looking for
- [distance] is the allowed Levenshtein distance between the word we're looking for and the ones we detect in the text (to mitigate OCR errors) (default is 0)

## neighbors.py
This script computes the most frequent neighbors (words appearing next to) of a word.
```
python neighbors.py in_csv word neighborhood [dist] [top_k]
```
where:
- in_csv is a csv containing a "text" column where the neighbors will be looked out for (e.g. df_treated.csv, for the whole corpus)
- word is the word we're looking the neighbors of
- [dist] is the allowed Levenshtein distance between our word and the corpus words (to mitigate OCR errors) (default is 0)
- [top_k] is the number of returned neighbors (default is 10)

## ner.py
This script is a first try at performing Named Entity Recognition on one magazine's issue. It works but is very basic and needs tuning to be correctly exploitable.
```
python ner.py in_csv month
```
where:
- in_csv is a csv containing a "text" column for which the ner will be performed (e.g. df_treated.csv, for the whole corpus
- month is the magazine's issue where the NER has to be performed, starting at 0 for January 1970, 1 for February 1970... 12 for January 1971...
Pay attention: The script prints its output, but only store it partially, more work is needed for a complete store allowing for a clean load

## occurrences_month.py
This script computes the occurrences of a word for each different month (or issue of the magazine)
```
python occurrences_month.py in_csv word [distance] [deviation]
```
where:
- in_csv is "df_treated.csv", or a similar dataframe
- word is the word we're looking out for
- [distance] is the allowed Levenshtein distance between our words and the corpus words (to mitigate OCR errors) (default is 0)
- [deviation] is a mean-deviating factor from which the column on the output picture will be highlighted (default is 3)

## occurrences_year.py
This script computes the occurrences of a word for each different year
```
python occurrences_year.py in_csv word [distance] [deviation]
```
where:
- in_csv is "df_treated.csv", or a similar dataframe
- word is the word we're looking out for
- [distance] is the allowed Levenshtein distance between our words and the corpus words (to mitigate OCR errors) (default is 0)
- [deviation] is a mean-deviating factor from which the column on the output picture will be highlighted (default is 3)

## page_occ_year.py
This script computes the number of pages where a word appear for each different year
```
python page_occ_year.py in_folder word [distance]
```
- in_csv is "pages_treated_txts", or a similar folder
- word is the word we're looking out for
- [distance] is the allowed Levenshtein distance between our words and the corpus words (to mitigate OCR errors) (default is 0)

## textblob_sent_analysis_month.py
This script tries to output a sentiment analysis associated to a word for each issue of the magazine. It should probably not be used as is, as it uses the textblob model which was not trained on a similar corpus as ours.
```
python textblob_sent_analysis_month.py in_csv word half_size [dist]
```
where:
- in_csv is "df_treated.csv" or a similar file
- word is the word we want to analyze the sentiment for
- half_size is half the size of the blob of text around our word that will be sentiment analyzed
- [dist] is the allowed Levenshtein distance between our words and the corpus words (to mitigate OCR errors) (default is 2)

## textblob_sent_analysis_year.py
This script tries to output a sentiment analysis associated to a word for each year the magazine was issued. It should probably not be used as is, as it uses the textblob model which was not trained on a similar corpus as ours.
```
python textblob_sent_analysis_month.py in_csv word half_size [dist]
```
- in_csv is "df_treated.csv" or a similar file
- word is the word we want to analyze the sentiment for
- half_size is half the size of the blob of text around our word that will be sentiment analyzed
- [dist] is the allowed Levenshtein distance between our words and the corpus words (to mitigate OCR errors) (default is 2)
