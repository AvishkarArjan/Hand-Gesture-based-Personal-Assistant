import cv2
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier
import numpy as np
import math
import webbrowser
import os
import time
import multiprocessing
# Volume 
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
# Brightness
import screen_brightness_control as screen
# Screenshot
import pyscreenshot 
# Music
from playsound import playsound
import multiprocessing
import threading

from PIL import Image
import tkinter as tk
from tkinter import Tk
from functions_ import ImageViewerApp, MusicPlayer


def take_ss():
    image_name = f"screenshot-{str(time.time())}"
    print(image_name+"********")
    filepath = fr"C:\Users\Avishkar Arjan\Pictures\Screenshots\{image_name}.png"    
    screenshot = pyscreenshot.grab()
    screenshot.save(filepath)
    print(filepath)

def inc_bright():
    get = screen.get_brightness()
    screen.set_brightness (get[0]+10)
    print (get)

def dec_bright():
    get = screen.get_brightness()
    screen.set_brightness (get[0]-10)
    print (get)

devices = AudioUtilities.GetSpeakers()
interface = devices. Activate (IAudioEndpointVolume. _iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

def inc_vol():
    current = volume.GetMasterVolumeLevel()
    if current+3.0 >= 0.0:
        return
    volume.SetMasterVolumeLevel(current + 3.0, None)

def dec_vol():
    current = volume.GetMasterVolumeLevel()
    if current-3.0 <= -65.0:
        return
    volume.SetMasterVolumeLevel(current - 3.0, None)

def show_pics():
    try:
        root = tk.Tk()
        root.title("Image Viewer")
        
        image_folder = r"C:\Users\Avishkar Arjan\Pictures\Screenshots"
        app = ImageViewerApp(root, image_folder)

        root.mainloop()
    except:
        print("Pic loop already running")

def play_music():
    try:
        root = tk.Tk()
        player = MusicPlayer(root)
        player.play_music()
        root.mainloop()
        
    except:
        print("Music playing...")


cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.5,maxHands=2)
# classifier = Classifier("Model/keras_model.h5", "Model/labels.txt")
classifier_left = Classifier("Model/model_left/keras_model.h5", "Model/model_left/labels.txt")
classifier_right = Classifier("Model/model_right/keras_model.h5", "Model/model_right/labels.txt")
offset = 20
imgSize = 300

labels = ["A","B","C","Calc","D","F","G","L","Music","SS","Thumb_up","Thumb_down","V_up","V_down","W","Y"]
labels_left = ["Thumb_up","Thumb_down","V_up","V_down","SS","M","Calc"]
labels_right = ["A","B","C","D","F","G","L","W","Y"]
while True:
    success, img = cap.read()
    imgOutput = img.copy()
    hands, img = detector.findHands(img, draw=True, flipType=True)

    if hands:
        hand1 = hands[0]
        handType = hand1["type"]
        print(handType)
        # bounding box info
        lmList1= hand1["lmList"]
        x, y, w, h = hand1["bbox"]
        imgCrop = img[
            y - offset : y + h + offset, x - offset : x + w + offset
        ]  # cropped part of the hand

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        if handType == "Right":
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)

                imgWhite[:, wGap : wCal + wGap] = imgResize
                prediction, index = classifier_right.getPrediction(imgWhite, draw=False)
                cv2.putText(imgOutput, labels_right[index], (x,y-20), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255), 2)
                
                
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)

                imgWhite[hGap : hCal + hGap, :] = imgResize
                prediction, index = classifier_right.getPrediction(imgWhite, draw=False)
                cv2.putText(imgOutput, labels_right[index], (x,y-20), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255), 2)

            if index == 0:
                time.sleep(1)
                os.startfile(r"C:\Windows\System32\notepad.exe")
                time.sleep(2)
            elif index == 1:
                time.sleep(1)
                os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk")
                time.sleep(2)
            elif index == 2:
                time.sleep(1)
                os.startfile(r"C:\Windows\System32\calc.exe")
                time.sleep(1)
            elif index == 3:
                # webbrowser.open("https://www.google.com")
                # os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk")
                
                # thread_1 = threading.Thread(target=show_pics)
                # thread_1.start()
                time.sleep(1)
                thread_1 = threading.Thread(target=play_music)
                thread_1.start()
                time.sleep(2)
                # time.sleep(5)
            elif index == 5:
                time.sleep(1)
                os.startfile(r"C:\Users\Avishkar Arjan\Pictures\Screenshots")
                time.sleep(2)

            elif index==6:
                time.sleep(1)
                webbrowser.open("https://www.google.com")
                time.sleep(2)
            elif index == 7:
                time.sleep(1)
                os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk")
                time.sleep(2)
            elif index == 8:
                time.sleep(1)
                webbrowser.open("https://www.youtube.com")
                time.sleep(2)

        else:
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)

                imgWhite[:, wGap : wCal + wGap] = imgResize
                prediction, index = classifier_left.getPrediction(imgWhite, draw=False)
                cv2.putText(imgOutput, labels_left[index], (x,y-20), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255), 2)

                # print(prediction, index)
                
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)

                imgWhite[hGap : hCal + hGap, :] = imgResize
                prediction, index = classifier_left.getPrediction(imgWhite, draw=False)
                cv2.putText(imgOutput, labels_left[index], (x,y-20), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255), 2)

            if index == 0:
                inc_bright()
            elif index == 1:
                dec_bright()
            elif index == 2:
                inc_vol()
            elif index == 4:
                time.sleep(1)
                take_ss()
                time.sleep(2)

            
        print(prediction,index)
        cv2.imshow("ImageWhite", imgWhite)

        

        
        cv2.rectangle(imgOutput, (x-offset,y-offset), (x+w+offset, y+h+offset), (255,0,255), 4)
    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)

    

