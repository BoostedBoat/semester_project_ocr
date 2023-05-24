# python jpg_to_pdf_file.py in_path out_path [true | false]

import cv2
import pytesseract
import sys
from PIL import Image
import numpy as np
import PyPDF2
import os
import io
import img2pdf
from PIL import Image

def resize(path):
    im = Image.open(path)
    im = im.save("./temp_300.tiff", dpi=(300, 300))

#skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def preprocess(img):
    contrasted = cv2.convertScaleAbs(img, alpha=0.94, beta=0.1)

    #scale = 1
    #resized = cv2.resize(img, (int(img.shape[1]*scale), int(img.shape[0]*scale)), interpolation=cv2.INTER_AREA)

    gray = cv2.cvtColor(contrasted, cv2.COLOR_BGR2GRAY)

    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

    blur = cv2.GaussianBlur(denoised, (7,7), 0)

    #thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #bin = 255 - thresh
    #th, bin = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    bin = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)

    #kernel = np.ones((3,3), np.uint8)
    #eroded = cv2.erode(bin, kernel, iterations=1) 
    #dilated = cv2.dilate(eroded, kernel, iterations=1)

    #deskewed = deskew(bin)

    return bin

def get_conf_total(preprocessed, config):
    data = pytesseract.image_to_data(preprocessed, lang='fra', output_type = 'data.frame', config=config)
    #string_data = pytesseract.image_to_string(bin)

    data_filtered = data[data.conf != -1]
    sum_confidence = data_filtered['conf'].sum()

    return sum_confidence, len(data_filtered['conf'])

in_path = sys.argv[1]
out_path = sys.argv[2]

get_confidence = False

if(len(sys.argv) > 3):
    get_confidence = sys.argv[3]

up_dir = os.listdir(in_path)

for ud in up_dir:

    dir = os.listdir(in_path + '/' + ud)

    pdf_writer = PyPDF2.PdfWriter()
    total_conf = 0
    nbr_of_words = 0

    txtFile = open(out_path + '/' + ud + '.txt', 'w')

    for p in dir:
        print(p)
        img = cv2.imread(in_path + '/' + ud + '/' + p)
        preprocessed = preprocess(img)
        #to_app = True
        is_img = False
        config = "--psm 1 -c tessedit_char_blacklist=|_"
        if(get_confidence):
            t, n = get_conf_total(preprocessed, config)
            if n!= 0:
                print(t/n)
                print(n)
            if n != 0 and t/n < -10:
                is_img = True
            else:
                total_conf += t
                nbr_of_words += n
            #if t/n > 65:
                #to_app = False
        if not is_img:
            text = pytesseract.image_to_string(preprocessed, lang='fra', config=config)
            txtFile.write(text)
            page = pytesseract.image_to_pdf_or_hocr(preprocessed, lang='fra', config=config, extension='pdf')
            pdf = PyPDF2.PdfReader(io.BytesIO(page))
            #pdf_writer.add_page(pdf.pages[0])
            #if to_app:
            pdf_writer.append(pdf)

    txtFile.close()

    pdf_writer.write(out_path + '/' + ud + '.pdf')
    pdf_writer.close()
    #with open(out_path, 'wb') as f:
        #f.write(imgs)

    if(get_confidence):
        c = total_conf/nbr_of_words
        print(ud)
        print("Mean confidence : " + str(c))
        print("Total nbr of words : " + str(nbr_of_words))

#text_f = open(out_path, 'w')
#text_f.write(string_data)
#text_f.close()