# txt_management

This folder contains python scripts aimed at managing the text we get from the OCR. It treats it and makes it more understandable and useful for the data mining part.

## convert_folder.py
This script converts a raw OCR txt output to a treated one.
```
python convert_folder.py in_folder out_folder [1|0]
```
where:
- in_folder is the path to the folder where the raw inputs are stored
- out_folder is the path to the folder where the treated outputs will be stored
- [1|0]: 1 if lines should be concatenated (ending up in one big block of text), 0 if lines should not be concatenated (preserves end of lines)

## txt_management.py
This script contains helper functions for convert_folder.py

## stopwords.txt
A list of stopwords that will be excluded from the treated txts.
