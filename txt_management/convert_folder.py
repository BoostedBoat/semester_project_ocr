#python convert_folder.py in_folder out_folder [1|0]

import sys
import os
import txt_management

in_folder = sys.argv[1]
out_folder = sys.argv[2]
treat_text = True
if len(sys.argv) > 3:
    treat_text = sys.argv[3]

if not os.path.exists(out_folder):
        os.mkdir(out_folder)

dir = os.listdir(in_folder)

for t in dir:
    print(t)
    in_file = in_folder + "/" + t
    out_file = out_folder + "/" + t
    txt_management.treat_text(in_file, out_file, treat_text)
