import sys

import numpy as np
import cv2
from HelperFunction import removeDuplicateLine
import matplotlib.pyplot as plt
from HelperFunction import trebleLocation
from HelperFunction import displayText



note = cv2.CascadeClassifier('fullquater.xml')
treble = cv2.CascadeClassifier('treble.xml')
bass = cv2.CascadeClassifier('bass.xml')

img = cv2.imread('musicsheet/testing.png')
dimension = img.shape
height = dimension[0]
width = dimension[1]
resized = cv2.resize(img, (width+2000, height+2000))
dimension = resized.shape
height_resize = dimension[0]
width_resize = dimension[1]
gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
before = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sheet = cv2.cvtColor(before,cv2.COLOR_GRAY2BGR)
line_edge = cv2.Canny(sheet,50,150,apertureSize=3)
lines = cv2.HoughLines(line_edge,1,np.pi/180,250)

notes = note.detectMultiScale(gray,1.20,5)
trebles = treble.detectMultiScale(gray,1.20,5)
basses = bass.detectMultiScale(gray,1.20,5)


resized = cv2.resize(img, (width, height))

def Rectangle(notes):
    for (x, y, w, h) in notes:
        x1 = x * width / width_resize
        y1 = y * height / height_resize
        w1 = w * height /height_resize
        h1 = h * height / height_resize
        cv2.rectangle(sheet, (int(x1), int(y1)), (int(x1) + int(w1), int(y1) + int(h1)), (255, 0, 0), 1)

staffLine = removeDuplicateLine(lines)

axisY = []
for (x, y, w, h) in trebles:
    y1 = y * height / height_resize
    axisY.append(y1)
trebleY = trebleLocation(axisY, staffLine)

print(trebleY)


Rectangle(notes)
Rectangle(trebles)
Rectangle(basses)
plt.imshow(sheet)
plt.show()
space = staffLine[0][1] - staffLine[0][0]
def checkScore(notes):
    for (x, y, w, h) in notes:
        x1 = x * width / width_resize
        y1 = y * height / height_resize
        x1 = int(round(x1))
        y1 = int(round(y1))
        for treble in trebleY:
            print('treble',treble)
            if treble[0] - space <= y1 <= treble[4] + space:
                for i in range(0,len(treble)):
                    if  treble[i] - 4 <= y1 <= treble[i] + 2:
                        if i == 0:
                            displayText(sheet,'E2',x1,y1-3)
                            print("E2")
                        if i == 1:
                            displayText(sheet, 'C2', x1,y1-3)
                            print("C2")
                        if i == 2:
                            displayText(sheet, 'A2', x1,y1-3)
                            print("A1")
                        if i == 3:
                            displayText(sheet, 'F2', x1,y1-3)
                            print("F1")
                    elif treble[i] + 5 <= y1 <= treble[i] + 10:
                        if i == 0:
                            displayText(sheet,'D2',x1,y1-3)
                            print("D2")
                        if i == 1:
                            displayText(sheet, 'B2', x1,y1-3)
                            print("B2")
                        if i == 2:
                            displayText(sheet, 'G1', x1,y1-3)
                            print("G1")
                        if i == 3:
                            displayText(sheet, 'E1', x1,y1-3)
                            print("E1")

            else:
                pass



for (x, y, w, h) in notes:
        x1 = x * width / width_resize
        y1 = y * height / height_resize


checkScore(notes)
cv2.imshow('line', sheet)
cv2.waitKey(0)
cv2.destroyAllWindows()