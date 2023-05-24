from nltk.corpus import stopwords
from nltk import word_tokenize
import string

def treat_lines(txt, nbr=0):
    sw = set(stopwords.words('french') + list(string.punctuation))
    return [i for i in word_tokenize(txt.lower()) if i not in sw and len(i) > nbr]

def treat_text(in_path, out_path, with_lines=1):
    inTxt = None
    with open(in_path) as file:
        inTxt = file.readlines()

    entire_text = ""

    for line in inTxt:
        no_newline = line[:len(line)-1]
        if len(no_newline) > 0:
            no_dash = no_newline
            if (no_newline[-1] == '-'):
                no_dash = no_newline[:len(no_dash)-1]
            else:
                no_dash = no_newline + " "
            entire_text = entire_text + no_dash

    if int(with_lines) == 1:
        entire_text = treat_lines(entire_text, 2)

    outTxt = open(out_path, 'w')

    if int(with_lines) == 1:
        for entry in entire_text:
            outTxt.write(entry + " ")
    else:
        outTxt.write(entire_text)

    outTxt.close()

