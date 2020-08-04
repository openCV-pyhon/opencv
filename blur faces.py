import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('cascade path')

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

while True:
    success, img = cap.read()
    blured = img.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, (1+(17/1000)), 6)
    
    for (x,y,w,h) in faces:
        area = w*h
        minArea = 5797
        if area >minArea:
            blured = cv2.rectangle(blured, (x,y), (x+w, y+h), (255,0,0), 2)
            blured[y:y+h, x:x+w] = cv2.blur(blured[y:y+h, x:x+w], (23, 23))
    
    imgStack = stackImages(0.8,([img, blured]))
    #cv2.imwrite('C:/Users/borst/Downloads/www.shutterstock.com/de/image-photo/collage-many-different-human-faces-164747228/4.jpg', blured)
    
    cv2.imshow("Result", imgStack)
    if cv2.waitKey(1) & 0xFF == ord('q'):
         break
