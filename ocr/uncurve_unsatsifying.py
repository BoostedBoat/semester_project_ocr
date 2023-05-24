# python uncurve_unsatisfying.py in_path out_path

import cv2
import numpy as np
import csv
import sys
import os
import time
import pandas as pd
from pygam import GAM, LinearGAM, s, f, te

def load_img(path):
    return cv2.imread(path)

def to_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def otsu_thresh(grayscale):
    return cv2.threshold(grayscale, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def scatterplot(thresholded):
    scatterplot_cvs = open('./scatterplot_temp.cvs', 'w')

    writer = csv.writer(scatterplot_cvs)
    writer.writerow(['X', 'Y'])

    for x in range(thresholded.shape[0]):
        for y in range(thresholded.shape[1]):
            #search for black pixels
            if (thresholded[x][y] < 128):
                writer.writerow([y, thresholded.shape[0] - x])

    scatterplot_cvs.close()

    df = pd.read_csv('./scatterplot_temp.cvs', sep=',')

    os.remove('./scatterplot_temp.cvs')

    return df

def get_GAM(image, thresholded, scatterplot_df, n_splines):
    img_copy = image.copy()
    predictors = ['X']
    outcome = ['Y']
    X = scatterplot_df[predictors].values
    y = scatterplot_df[outcome]
    gam = LinearGAM(n_splines = n_splines)
    gam.gridsearch(X, y)

    y_hat = gam.predict(np.linspace(0, thresholded.shape[1], num=thresholded.shape[1]))

    for i in range(image.shape[1]):
        img_copy[:, i, 0] = np.roll(image[:, i, 0], round(y_hat[i] - thresholded.shape[0]/2))
        img_copy[:, i, 1] = np.roll(image[:, i, 1], round(y_hat[i] - thresholded.shape[0]/2))
        img_copy[:, i, 2] = np.roll(image[:, i, 2], round(y_hat[i] - thresholded.shape[0]/2))

    return img_copy

def save_img(path, image):
    cv2.imwrite(path, image)

in_path = sys.argv[1]
out_path = sys.argv[2]

img = load_img(in_path)
grayscale = to_grayscale(img)
otsu = otsu_thresh(grayscale)
sp = scatterplot(otsu)
uncurved = get_GAM(img, otsu, sp, 4)
save_img(out_path, uncurved)