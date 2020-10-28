import sys
import numpy as np
import cv2
from HelperFunction import *
import matplotlib.pyplot as plt
from LineDetection import lineDetection
import time
from Remover import *
from StackingFunction import *
from copy import deepcopy

start_time = time.time()

note = cv2.CascadeClassifier('q13.xml')
treble = cv2.CascadeClassifier('treble20.xml')
bass = cv2.CascadeClassifier('bass14.xml')
sharp = cv2.CascadeClassifier('sharp27.xml')
flat = cv2.CascadeClassifier('flat13.xml')
quat = cv2.CascadeClassifier('fullnote.xml')
fullquat = cv2.CascadeClassifier('fullquat3.xml')
img = cv2.imread('musicsheet/testing.png')


# line = lineDetection(img)
# dimension = img.shape
# height = dimension[0]
# width = dimension[1]
# img = img[line[0] - 50:line[len(line)-1] + 50, 0:width]

dimension = img.shape
height = dimension[0]
width = dimension[1]

line = lineDetection(img)
# print(line)
# image processing
grayOrigin = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


resized = cv2.resize(img, (width+2200, height+2200))
plt.imshow(resized)
plt.show()
# cv2.imwrite('Result/lineDetetion.jpg', img)
dimension = resized.shape
height_resize = dimension[0]
width_resize = dimension[1]
gray = cv2.cvtColor(resized,cv2.COLOR_BGR2GRAY)
before = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sheet = cv2.cvtColor(before,cv2.COLOR_GRAY2BGR)
ret, otsu = cv2.threshold(grayOrigin,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# cv2.imwrite('Otsu/ex2.jpg', otsu)
# cv2.imshow('sheet', otsu)
# line_edge = cv2.Canny(sheet,50,150,apertureSize=3)
# lines = cv2.HoughLines(line_edge,1,np.pi/180,250)

notes = note.detectMultiScale(gray,1.20,3)
trebles = treble.detectMultiScale(gray,1.20,5)
basses = bass.detectMultiScale(gray,1.20,2)
sharps = sharp.detectMultiScale(gray,1.20,3)
flats = flat.detectMultiScale(gray,1.20,2)
quats = quat.detectMultiScale(gray,1.20,3)
fullquats = fullquat.detectMultiScale(gray,1.20,3)

resized = cv2.resize(img, (width, height))
removeDup = removeDuplicate(line)
space = findSpace(removeDup)
# print(removeDup)
staffLine = createStaffline(removeDup, space)
notes, stacks = groupUpNote(notes)
quats, stackQuat = groupUpNote(quats)


# sharps = removeDuplicateSharp(sharps)

countSharpsFlats(staffLine,basses, trebles,False,sharps,width,width_resize,height,height_resize)
# sharps = np.array(sharps)
countSharpsFlats(staffLine,basses, trebles,True,flats,width,width_resize,height,height_resize)
# flats = np.array(flats)
BassLoc = getTrebleBassLoc(basses, staffLine, height, height_resize, width, width_resize)
TrebleLoc = getTrebleBassLoc(trebles, staffLine, height, height_resize, width, width_resize)
# print(sharps)
# print('')
# print(notes)


# work
BassTreble = updateTrebleAndBassLoc(TrebleLoc,BassLoc)
TLoc = BassTreble[0]
BLoc = BassTreble[1]
print(TLoc)

def Rectangle(notes,color1,color2,color3):
    for (x, y, w, h) in notes:
        x1 = x * width / width_resize
        y1 = y * height / height_resize
        w1 = w * height /height_resize
        h1 = h * height / height_resize
        cv2.rectangle(sheet, (int(x1), int(y1)), (int(x1) + int(w1), int(y1) + int(h1)), (color1, color2, color3), 2)

# print(basses)

axisY = []
for (x, y, w, h) in trebles:
    currentX = []
    y1 = np.floor(y * height / height_resize)
    y2 = np.floor(y1 + w)
    currentX.append(y1)
    currentX.append(y2)
    axisY.append(currentX)

#
# Rectangle(quats,0,256,0) #green
# Rectangle(fullquats,256,0,0)#red
# Rectangle(flats,0,0,256)#blue
# Rectangle(notes,255,128,0)#sky blue
# Rectangle(trebles,255,51,255)#pink
# Rectangle(basses,255,51,153)#purple
# Rectangle(sharps,0,255,255)#yellow
# cv2.imshow('line2', sheet)

space = 0
for line in staffLine:
    if len(line[1]) > 2:
        space = line[1][1] - line[1][0]
        break
halfSpace = np.floor(space/2)
averageLocation = np.floor(space * 0.25)
Score(sheet,flats,sharps,notes,width,width_resize, height, height_resize,space,averageLocation,halfSpace,TLoc,BLoc)
Score(sheet,flats,sharps,quats,width,width_resize, height, height_resize,space,averageLocation,halfSpace,TLoc,BLoc)
Score(sheet,flats,sharps,fullquats,width,width_resize, height, height_resize,space,averageLocation,halfSpace,TLoc,BLoc)
scoreStack(stacks,sheet,flats,sharps,width,width_resize, height, height_resize,space,averageLocation,halfSpace,TLoc,BLoc)
scoreStack(stackQuat,sheet,flats,sharps,width,width_resize, height, height_resize,space,averageLocation,halfSpace,TLoc,BLoc)




# checkScore(notes)
print("--- %s seconds ---" % (time.time() - start_time))
cv2.imshow('line', sheet)
plt.imshow(sheet)
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
