import cv2
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import time
from HelperFunction import * 

start = time.time()
sharp = cv2.CascadeClassifier('sharp26.xml')
img = cv2.imread('musicsheet/yankee.jpg')

grayOrigin = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
dimension = img.shape
height = dimension[0]
width = dimension[1]
resized = cv2.resize(img, (width+2500, height+2500))
dimension = resized.shape
height_resize = dimension[0]
width_resize = dimension[1]
gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
before = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sheet = cv2.cvtColor(before,cv2.COLOR_GRAY2BGR)
sharps = sharp.detectMultiScale(gray,1.20,3)

def Rectangle(notes):
    for (x, y, w, h) in notes:
        x1 = x * width / width_resize
        y1 = y * height / height_resize
        w1 = w * height /height_resize
        h1 = h * height / height_resize
        cv2.rectangle(sheet, (int(x1), int(y1)), (int(x1) + int(w1), int(y1) + int(h1)), (255, 0, 0), 1)


def removeDuplicaeSharp(sharps):
    coordinates = np.array(sharps).tolist()
    clone = deepcopy(coordinates)
    for sharp in coordinates:
        x = sharp[0]
        y = sharp[1]
        w = sharp[2]
        h = sharp[3]
        if sharp in clone:
            for current in coordinates:
                cx = current[0]
                cy = current[1]
                cw = current[2]
                ch = current[3]
                if cy < y and (cy + h) > y and cx - 5 < x < cx + 5:
                    if current in clone:
                        clone.remove(current)
                        break
                    else:
                        break
                if y + 100  < cy :
                    break
    return clone


def ScoreTest(sheet,flat,sharp, notes, width, width_resize, height, height_resize, space, averageLocation, halfSpace, trebles, basses):
    flat = np.array(flat).tolist()
    sharp = np.array(sharp).tolist()
    for (x, y, w, h) in notes:
        x1 = x * width / width_resize
        y1 = y * height / height_resize
        x1 = int(round(x1))
        y1 = int(round(y1))
        for bass in basses:
            if (x1 > bass[0][2]) and (x1 < bass[0][3]) and (
                    bass[1][0] - (space * 5) + (averageLocation * 2) <= y1 <= bass[1][len(bass[1]) - 1] + (
                    space * 5)) + (averageLocation * 2):
                trebleBassScore(y1,x1,True)



def trebleBassScore(x1,y1, isBass, flats, sharps,space,averageLocation,halfSpace,sheet,width,width_resize,height,height_resize):




plt.imshow(resized)
print(sharps)
# sharps = removeDuplicaeSharp(sharps)

Rectangle(sharps)
# plt.imshow(sheet)
plt.show()
cv2.imshow('line', sheet)
print("--- %s seconds ---" % (time.time() - start))
cv2.waitKey(0)
cv2.destroyAllWindows()