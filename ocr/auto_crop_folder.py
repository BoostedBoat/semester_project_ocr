# python auto_crop_folder.py in_folder out_folder
# https://stackoverflow.com/questions/72202507/how-to-crop-image-to-only-text-section-with-python-opencv

import cv2
import sys
import os

scale = 0.2

def pipeline(img):

    # Load image, grayscale, Gaussian blur, Otsu's threshold
    original = img.copy()

    '''imageR = cv2.resize(original, (int(original.shape[1] * scale), int(original.shape[0]*scale)))
    cv2.imshow('image', imageR)'''

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
    blur = cv2.GaussianBlur(denoised, (3, 3), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    #ret,ithresh = cv2.threshold(blur,200,255,cv2.THRESH_BINARY)
    #thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    #thresh = 255 - ithresh

    '''threshR = cv2.resize(thresh, (int(thresh.shape[1] * scale), int(thresh.shape[0]*scale)))
    cv2.imshow('thresh', threshR)'''

    # Remove horizontal lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,1))
    detected_lines = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
    cnts = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        cv2.drawContours(thresh, [c], -1, 0, -1)

    # Dilate to merge into a single contour
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30,30))
    dilate = cv2.dilate(thresh, vertical_kernel, iterations=3)

    #dilate = 255 - dilate

    '''dilateR = cv2.resize(dilate, (int(dilate.shape[1] * scale), int(dilate.shape[0]*scale)))
    cv2.imshow('dilate', dilateR)'''

    # Find contours, sort for largest contour and extract ROI
    ROI = original
    cnts, _ = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:-1]
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        cv2.rectangle(img, (x, y), (x + w, y + h), (36,255,12), 4)
        ROI = original[y:y+h, x:x+w]
        break

    '''roiR = cv2.resize(ROI, (int(ROI.shape[1] * scale), int(ROI.shape[0]*scale)))
    cv2.imshow('ROI', roiR)'''

    o_rows,o_cols,_ = original.shape
    r_rows, r_cols,_ = ROI.shape

    toRet = ROI
    if ((r_rows*r_cols < 0.5*o_rows*o_cols)):
        toRet = original
    
    #cv2.waitKey(0)

    return toRet

in_path = sys.argv[1]
out_path = sys.argv[2]

dir = os.listdir(in_path)

for d in dir:
    print(d)
    if not os.path.exists(out_path + '/' + d):
        os.mkdir(out_path + '/' + d)
    files = os.listdir(in_path + '/' + d)
    for f in files:
        print(f)
        img = cv2.imread(in_path + '/' + d + '/' + f)
        cropped_i = pipeline(img)
        cv2.imwrite(out_path + '/' + d + '/' + f , cropped_i)
        #cv2.waitKey(0)
