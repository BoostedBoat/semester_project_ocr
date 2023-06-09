# dataframe

This folder contains python scripts aimed at creating and initializing the dataframes in which the dataset is stored. There are two kinds of dataframes, one containing one entry per magazine (a big block of text), one containing one entry per page per magazine, which exists for each magazine separately and is divided and organized in folders and subfolders.

## corpus_to_df.py
This script converts a text file to the first kind of dataframe.
```
python corpus_to_df.py in_csv in_folder
```
where:
- in_csv is the dataframe in which the data will be stored
- in_folder is the folder containing the text files that will be put in the dataframe
Pay attention, the in_folder has to be organized in a specific way: it's a root folder containing one subfolder per year, each containing one file per magazine issue. Missing issues must be replaced by empty text files, else the datafram won't be filled correctly (e.g., if the August magazine is missing, an empty txt file must take its place). Moreover, those text files should be ordered by date of publication (January, then February, then March...)

## create_dataframe.py
This script creates an empty file, being the first kind of dataframe (that'll have to be fileld by the corpus_to_df.py script).
```
python create_dataframe.py out_path
```
where:
- out_path is the name of the created dataframe.

## df_helpers.py
This file contains useful methods for the conversion from text files to dataframes. It can't be used in standalone.

## get_pages_from_pdfs.py
This script is responsible for the creation of all the dataframes of the second kind.
```
python get_pages_from_pdfs.py in_folder out_folder_raw out_folder_treated
```
where:
- in_folder is a folder containing searchable pdfs (obtained throught the OCR process) from which we want to extract the per-page dataframes. One dataframe will be created per pdf
- out_folder_raw is the folder in which will be stored the dataframes containing the untreated text data from the pdfs
- out_folder_treated is the folder in which will be stored the dataframes containing the treated text data from the pdfs

## txt_to_df.py
This script adds one text file in a specific place in the dataframe created by the create_dataframe.py script
```
#python txt_to_df.py in_csv year month in_text
```
where:
- in_csv is the csv in which the text will be placed
- year is the year at which it will be added (1970 to 1985)
- month is the month at which it will be added (1 for January, 2 for February...)
- in_text is the text to be added (in general the text from the issue corresponding the the preceding month and year)

## year_to_df.py
This script adds a whole year worth of text files in a specific place in the dataframe created by the create_dataframe.py script
```
#python year_to_df.py in_csv in_folder year
```
where:
- in_csv is the csv in which the texts will be placed
- in_folder is the folder in which the texts are placed (Pay attention: one per month, include empty entries if necessary, sorted in chronological order)
- year is the year at which the texts will be added (1970 to 1985), their place in the dataframe


