import cv2
import numpy as np
import time
import imutils

cascade_path = cv2.CascadeClassifier('cascade path')
frameWidth = 640
frameHeigth = 480

count = 0

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeigth)

def empty(a):
    pass

#Trackbar
cv2.namedWindow('Result')
cv2.resizeWindow('Result', frameWidth, frameHeigth+100)
cv2.createTrackbar('Scale', 'Result', 17, 1000, empty)
cv2.createTrackbar('Neig', 'Result', 6, 50, empty)
cv2.createTrackbar('Min Area', 'Result', 5797, 100000, empty)
cv2.createTrackbar('Brightness', 'Result', 180, 255, empty)

while True:
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cameraBrightness = cv2.getTrackbarPos('Brightness', 'Result')
    cap.set(10, cameraBrightness)
    scaleVal =1 + (cv2.getTrackbarPos("Scale", "Result") /1000)
    neig=cv2.getTrackbarPos("Neig", "Result")
    humans = cascade_path.detectMultiScale(gray, scaleVal, neig)

    height, width = img.shape[0:2]
    text1 = ('Humans count : '+ str(count))
    cv2.putText(img, text1, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2)

    img = cv2.line(img, (0, height-240), (width, height-240), (255,0,0), 2,)

    #image = cv2.line(image, start_point, end_point, color, thickness) 

    for (x,y,w,h) in humans:
        area = w*h
        org = x,y
        var1 = int(y+h/2)
        var2 = height-240
        minArea = cv2.getTrackbarPos("Min Area", "Result")
        if area >minArea:
            if (var1<var2+6 and var1>var2-6):
                count += 1
            img = cv2.rectangle(img, (x,y), (x+w, y+h), (20,114,222), 3)
            img = cv2.putText(img, 'Human', org, cv2.FONT_HERSHEY_SIMPLEX, 1, (20,114,222), 2)
            roi_color = img[y:y+h, x:x+w]

            

    cv2.imshow("Result", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break
