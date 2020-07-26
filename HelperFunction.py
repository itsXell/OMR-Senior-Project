import cv2
import numpy as np

def Rectangel(img,notes,width,height, resizedWidth, resizeHeight):
    for (x, y, w, h) in notes:
        x1 = x * width / resizedWidth
        y1 = y * height / resizeHeight
        w1 = w * height / resizeHeight
        h1 = h * height / resizeHeight
        new_img = cv2.rectangle(img, (int(x1), int(y1)), (int(x1) + int(w1), int(y1) + int(h1)), (255, 0, 0), 1)
        return new_img

def trebleLocation(treblesY, staffLines):
    loc = []
    for treble in treblesY:
        for staffLine in staffLines:
            if len(staffLine) == 5:
                if treble >= staffLine[0] - 5 and treble <= staffLine[4] + 3:
                    loc.append(staffLine)
                    break
    return loc
    space = staffline[0][0] - staffline[0][1]


font = cv2.FONT_HERSHEY_SIMPLEX
def displayText(img,text,x,y):
    cv2.putText(img, text, (x, y), font, 0.5, (0, 0, 255), 1, cv2.LINE_AA)



def removeDuplicateLine(lines):
    x = []
    y = []
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = b * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * a)
        if x1 != 0 and x2 != 0:
            x.append(rho)
            y.append(theta)
            # cv2.line(sheet, (x1, y1), (x2, y2), (0, 0, 255), 1)
        else:
            pass
    x.sort()
    singleLine = []
    current = 0
    for i in x:
        if i - current > 5:
            current = i
            singleLine.append(i)
        else:
            pass

    staff_line = [[]]
    index = 0
    current = singleLine[0]
    currentList = []
    for line in singleLine:
        if line - current < 25:
            staff_line[index].append(line)
            current = line
        else:
            currentList = []
            index += 1
            currentList.append(line)
            staff_line.append(currentList)
            current = line
    # staff_line[0].remove(66)
    return staff_line