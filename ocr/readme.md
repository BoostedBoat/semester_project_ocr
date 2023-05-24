# OCR scripts

This folder contains script aimed at executing an OCR of JPGs pictures.
Warning: you should only use ASCII characters in the name of your script arguments.

# auto_crop_folder.py
This script automatically crops JPG pictures. It detects the text on the image and crops the picture around it. Pay attention, the automatic cropping sometimes loses a bit of information: e.g. titles of articles that are separated from the text by a blank text can sometimes be cropped out of the picture.
'''
python auto_crop_folder.py in_folder out_folder
'''
where:
- in_folder is a path to a folder containing one or several folders containing the JPG pictures
- out_folder is a path to a folder where the cropped JPG pictures will be stored

# get_pages_from_pdfs.py
This script transforms a searchable pdf into a pandas dataframe containing the text separated by page.
'''
python get_pages_from_pdfs.py in_folder out_folder_raw out_folder_treated
'''
where:
- in_folder is a path to a folder containing the pdfs
- out_folder_raw is a path to a folder where the untreated text will be stored
- out_folder_treated is a path to a folder where the treated (remove stopwords, remove end-of-line...) text will be stored

# jpg_to_pdf_folder.py
This script performs the OCR on JPGs (cropped or not).
'''
python jpg_to_pdf_folder.py in_path out_path [true | false]
'''
where:
- in_path is the path to a folder containing one or several folders containing the JPG picture, one pdf will be created for each subfolder
- out_path is the path to a folder where the created pdfs will be stored
- [true|false]: if true, a mean ocr confidence score will be printed by the algorithm for each pdf, if false, the score won't be printed

# uncurve_unsatisfying.py
This script is not finished, it's a trial to uncurve very curved pages to get to a better ocr score. It may not compile.
'''
python uncurve_unsatisfying.py in_path out_path
'''
where:
- in_path is the path to a curved jpg
- out_path is the path where the uncurved jpg will be stored
