# Tracing the emergence of American psychology in France through Psychologie magazine (1970-1980)

## Context

MICE is a project studying the reception of behavior therapy in the Francophone context between the early 60s and the 90s. This repository's objective is to provide the initiators of the MICE project with a series of tools aimed at simplifying the analysis of the "Psychologie" magazine, and the role it played in disseminating the behavior therapy to a large audience. To do so, I was provided with pictures of the pages of the said magazines for the 1970-1985 periodes, which I then OCR'd and mined.

## Architecture

- data_mining: This folder contains useful python scripts for the analysis of the magazines
- ocr: This folder contains python scripts used for the Optical Character Recognition of the magazines
- txt_management: This folder contains useful python scripts to treat the txts obtained through the OCR

## Libraries and dependences

- gensim (https://pypi.org/project/gensim/)
- nltk (https://www.nltk.org/)
- numpy (https://numpy.org/)
- opencv (https://opencv.org/)
- pandas (https://pandas.pydata.org/)
- pdf2image (https://pypi.org/project/pdf2image/)
- pillow (https://pypi.org/project/Pillow/)
- pprint (https://docs.python.org/3/library/pprint.html)
- pyLDAvis (https://pypi.org/project/pyLDAvis/)
- pypdf2 (https://pypi.org/project/PyPDF2/)
- tesseract (https://github.com/tesseract-ocr/tesseract)
- textblob (https://pypi.org/project/textblob/)
