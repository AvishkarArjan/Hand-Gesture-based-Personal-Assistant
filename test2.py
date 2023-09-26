import cv2
import numpy as np
import math
import webbrowser
import time

# Functions to resize and crop the hand region
def resize_and_crop_hand(imgCrop, imgSize):
    imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
    h, w, _ = imgCrop.shape
    aspectRatio = h / w

    if aspectRatio > 1:
        k = imgSize / h
        wCal = math.ceil(k * w)
        imgResize = cv2.resize(imgCrop, (wCal, imgSize))
        wGap = math.ceil((imgSize - wCal) / 2)
        imgWhite[:, wGap:wCal + wGap] = imgResize
    else:
        k = imgSize / w
        hCal = math.ceil(k * h)
        imgResize = cv2.resize(imgCrop, (imgSize, hCal))
        hGap = math.ceil((imgSize - hCal) / 2)
        imgWhite[hGap:hCal + hGap, :] = imgResize

    return imgWhite

cap = cv2.VideoCapture(0)
offset = 20
imgSize = 300
folder = "Data/C"
counter = 0
labels = ["A", "B", "C"]

while True:
    success, img = cap.read()
    imgOutput = img.copy()

    # Detect hands
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, imgThreshold = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    hands = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 10000:  # Filter out small contours (adjust this value as needed)
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
            boundingBox = cv2.boundingRect(approx)
            hands.append({"bbox": boundingBox})

    for hand in hands:
        # bounding box info
        x, y, w, h = hand["bbox"]
        imgCrop = img[y - offset: y + h + offset, x - offset: x + w + offset]  # cropped part of the hand
        imgWhite = resize_and_crop_hand(imgCrop, imgSize)

        # Perform your classification here (use 'imgWhite') instead of 'img' in the classifier
        # prediction, index = classifier.getPrediction(imgWhite, draw=False)
        prediction, index = np.random.choice(labels), np.random.randint(0, len(labels))

        print(prediction, index)

        cv2.imshow("ImageWhite", imgWhite)

        if index == 2:
            webbrowser.open("https://www.youtube.com")
            time.sleep(2)

        cv2.putText(imgOutput, labels[index], (x, y - 20), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 2)
        cv2.rectangle(imgOutput, (x - offset, y - offset), (x + w + offset, y + h + offset), (255, 0, 255), 4)

    cv2.imshow("Image", imgOutput)
    key = cv2.waitKey(1)
