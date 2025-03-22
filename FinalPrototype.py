# Camera Imports
from PIL import Image
import pytesseract
import cv2
import os, sys, inspect #For dynamic filepaths
import numpy as np;

# Boom Gate imports
import RPi.GPIO as GPIO # type: ignore
from time import sleep

#Timestamp imports
import datetime;

#Timestamp Setup
licensePlates = {}
moneyOwedPerSecondStayed = 0.2
moneyOwed = 0.0

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


#Camera function for entering
def Check_Plate_Entry():
    
    print("Cam start")
    #Camera start
    cam = cv2.VideoCapture(0) 
    
    sleep(2)

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
        
        #Adds license plate and time to licensePlates dictionary if licence plate is 6 chars
        if filteredTextCount == 6:
            print(filteredText)
            licensePlates[filteredText] = datetime.datetime.now().timestamp()
            break


    #Turns off camera, stops video feed
    cam.release()
    cv2.destroyAllWindows()

    #Runs servo
    Open_Close()

#Camera function for exitting
def Check_Plate_Exit():
    
    print("Cam start")
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
        
        #Checks filtered text against lisencePlates, prints time and cost, removes filteredText from licesnsePlates
        if filteredTextCount == 6:
            print(filteredText)
            if filteredText in licensePlates:
                print("Time stayed was : ", round((licensePlates.get(filteredText) - datetime.datetime.now().timestamp())*-1, 2), " seconds.")
                moneyOwed = round((licensePlates.get(filteredText) - datetime.datetime.now().timestamp())*moneyOwedPerSecondStayed*-1, 2)
                print(moneyOwed, "$ owed")
                licensePlates.pop(filteredText)
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

#Line sensor run time (checking entry, checking exit)     
def Entry_Mode():
    print("Entry Mode")
    while True:
        if(GPIO.input(6) == False):
            print("Entering")
            Check_Plate_Entry()
            break
def Exit_Mode():
    print("Exit Mode")
    while True:
        if(GPIO.input(6)==False):
            print("Exiting")
            Check_Plate_Exit()
            break

Entry_Mode()
Exit_Mode()

        
#Cleanup for servo
pwm.stop()
GPIO.cleanup()

#Final message
print("done")
