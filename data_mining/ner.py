import spacy
from spacy import displacy
import sys
import pandas as pd

in_csv = sys.argv[1]

df = pd.read_csv(in_csv, index_col=0)

data_words = []

text = str(df.at[2, 'text'])
words = text.split(" ")

for w in words:
    data_words.append(w)

NER = spacy.load("fr_core_news_sm")

print(len(data_words))
doc= NER(' '.join(data_words))

all_labels = set()
all_persons = {}
all_locs = {}
all_misc = {}
all_orgs = {}
if doc.ents: 
    for ent in doc.ents: 
        #print(ent.text+' - ' +str(ent.start_char) +' - '+ str(ent.end_char) +' - '+ent.label_+ ' - '+str(spacy.explain(ent.label_))) 
        if ent.label_ == 'PER':
            if ent.text in all_persons:
                all_persons[ent.text] += 1
            else:
                all_persons[ent.text] = 1
        elif ent.label_ == 'MISC':
            if ent.text in all_misc:
                all_misc[ent.text] += 1
            else:
                all_misc[ent.text] = 1
        elif ent.label_ == 'ORG':
            if ent.text in all_orgs:
                all_orgs[ent.text] += 1
            else:
                all_orgs[ent.text] = 1
        elif ent.label_ == 'LOC':
            if ent.text in all_locs:
                all_locs[ent.text] += 1
            else:
                all_locs[ent.text] = 1
        all_labels.add(ent.label_)
else: 
    print('No named entities found.')

sorted_per = sorted(all_persons.items(), key=lambda x:x[1])
sorted_misc = sorted(all_misc.items(), key=lambda x:x[1])
sorted_loc = sorted(all_locs.items(), key=lambda x:x[1])
sorted_org = sorted(all_orgs.items(), key=lambda x:x[1])

print("\nPersons:")
print(sorted_per)
print("\nLocations:")
print(sorted_loc)
print("\nOrganisations:")
print(sorted_org)
print("\nMiscellaneous:")
print(sorted_misc)

print(all_labels)

config = NER.config
bytes_data = NER.to_bytes()

#print(config)

with open("ner_bytes_data.txt", "wb") as binary_file:
    # Write bytes to file
    binary_file.write(bytes_data)

'''with open("ner_config.ini", "wb") as configfile:
    # Write bytes to file
    config.write(configfile)'''