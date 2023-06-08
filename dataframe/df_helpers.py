import os

def add_one_entry(df, year, month, text):
    df.at[(year-1970)*12 + month-1,'text'] = text
    return df

def add_one_year(df, year, in_folder):
    dir = os.listdir(in_folder)

    month = 1
    for t in dir:
        print(t)
        in_file = in_folder + "/" + t

        print(in_file)
        text = None
        with open(in_file) as file:
            text = file.readlines()

        if len(text) != 0:
            df = add_one_entry(df, year, month, text[0])
        month += 1

    return df

