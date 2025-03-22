from PIL import Image
import pytesseract
import cv2
import os, sys, inspect #For dynamic filepaths
import numpy as np;
from time import sleep

cam = cv2.VideoCapture(0)

while True:
    check, frame = cam.read()

    img = cv2.resize(frame,(320,240))

    img_empty = np.zeros((img.shape[0], img.shape[1]))
    img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img2 = cv2.normalize(img1, img_empty, -300, 300, cv2.NORM_MINMAX)
    img3 = cv2.GaussianBlur(img2, (5, 5), 0)
    img4 = cv2.threshold(img3, 90, 255, cv2.THRESH_BINARY) [1]
    
    text = pytesseract.image_to_string(img4, config='--psm 6')

    #code from stackoverflow.com/questions/12767764/stripping-everything-but-alphanumeric-chars-from-a-string-in-python, answer from Ahmed Tremo
    filteredText = ""
    filteredTextCount = 0
    for c in text:
        if str.isalnum(c) and not str.islower(c):
            filteredText += c
            filteredTextCount += 1
    

    #cv2.imshow("Original", img)
    #cv2.imshow("Normalise", img2)
    #cv2.imshow("Blurred", img3)
    cv2.imshow("Threshold", img4)
    if 3 < filteredTextCount < 9:
        print(filteredText)
        break


    key = cv2.waitKey(1)
    if key == 27:
        break

sleep(5)
cam.release()
cv2.destroyAllWindows()