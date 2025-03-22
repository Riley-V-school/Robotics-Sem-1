# Camera Imports
from PIL import Image
import pytesseract
import cv2
import os, sys, inspect #For dynamic filepaths
import numpy as np;

# Boom Gate imports
import RPi.GPIO as GPIO # type: ignore
from time import sleep

#Board Setup
GPIO.setmode(GPIO.BCM)

#Servo, Line Sensor
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.IN)

#Definitions for Servo
pwm = GPIO.PWM(13, 50)
on = GPIO.output(13, True)
off = GPIO.output(13, False)
pwm.start(0)



#Camera function
def Check_Plate():
    
    #Camera start
    cam = cv2.VideoCapture(0) 
    
    #Camera function
    while True:
        check, frame = cam.read()

        #Filters
        img = cv2.resize(frame,(320,240))
        img_empty = np.zeros((img.shape[0], img.shape[1]))
        img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img2 = cv2.normalize(img1, img_empty, -300, 300, cv2.NORM_MINMAX)
        img3 = cv2.GaussianBlur(img2, (5, 5), 0)
        img4 = cv2.threshold(img3, 90, 255, cv2.THRESH_BINARY) [1]
        
        #Gets text
        text = pytesseract.image_to_string(img4, config='--psm 6')

        #Filters text
        filteredText = ""
        filteredTextCount = 0
        for c in text:
            if str.isalnum(c) and not str.islower(c):
                filteredText += c
                filteredTextCount += 1

        cv2.imshow("Image", img4)
        
        #Prints and breaks if image text is good
        if 3 < filteredTextCount < 9:
            print(filteredText)
            break

        #Breaks if escape is pressed
        key = cv2.waitKey(1)
        if key == 27:
            break

    #Turns off camera, stops video feed
    cam.release()
    cv2.destroyAllWindows()

    #Runs servo
    Open_Close()


#Open Close Function
def Open_Close():
    
    print("Opening")
    
    on
    pwm.ChangeDutyCycle(7)
    sleep(0.5)
    off
    pwm.ChangeDutyCycle(0)

    print("Waiting")
    sleep(3)
    
    on
    pwm.ChangeDutyCycle(2.5)
    sleep(0.5)
    off
    pwm.ChangeDutyCycle(0)

#Line sensor run time (checking)
while True:
    if(GPIO.input(6) == False):
        Check_Plate()
        break
    else:
        sleep(0.2)

#Cleanup for servo
pwm.stop()
GPIO.cleanup()

#Final message
print("Done")
sleep(1)
