def BassScore(basses,flat,sharps,x1,y1,space,averageLocation,halfSpace,sheet,width,width_resize,height,height_resize):
    for bass in basses:
        if (x1 > bass[0][2]) and (x1 < bass[0][3]) and (
                bass[1][0] - (space * 2) <= y1 <= bass[1][len(bass[1]) - 1] + (space * 2)):
            for i in range(0, len(bass[1]) - 1):
                sharp = ''
                for x, y, w, h in sharps:
                    sharpX = x * width / width_resize
                    sharpY = y * height / height_resize
                    sharpX = int(round(x1))
                    sharpY = int(round(y1))
                    if x1 - (w+20) <= sharpX <= x1 and sharpY - 50 > y1 < sharpY + h:
                        sharp = '#'
                if bass[1][i] - averageLocation <= y1 <= bass[1][i] + averageLocation:
                    for x, y, w, h in sharps:
                        sharpX = x * width / width_resize
                        sharpY = y * height / height_resize
                        sharpX = int(round(x1))
                        sharpY = int(round(y1))
                    if i == 0:
                        displayText(sheet, 'G'+sharp, x1, y1 - 3)
                        break
                    if i == 1:
                        displayText(sheet, 'E'+sharp, x1, y1 - 3)
                        break
                    if i == 2:
                        displayText(sheet, 'C'+sharp, x1, y1 - 3)
                        break
                    if i == 3:
                        displayText(sheet, 'A'+sharp, x1, y1 - 3)
                        break
                    if i == 4:
                        displayText(sheet, 'F'+sharp, x1, y1 - 3)
                        break
                elif bass[1][i] + halfSpace - averageLocation <= y1 <= bass[1][i] + halfSpace + averageLocation:
                    if i == 0:
                        displayText(sheet, 'F'+sharp, x1, y1 - 3)
                        break
                    if i == 1:
                        displayText(sheet, 'D'+sharp, x1, y1 - 3)
                        break
                    if i == 2:
                        displayText(sheet, 'B'+sharp, x1, y1 - 3)
                        break
                    if i == 3:
                        displayText(sheet, 'G'+sharp, x1, y1 - 3)
                        break
                    if i == 4:
                        displayText(sheet, 'E'+sharp, x1, y1 - 3)
                        break

                elif bass[1][i] - halfSpace - averageLocation <= y1 <= bass[1][i] - halfSpace + averageLocation:
                    if i == 0:
                        displayText(sheet, 'A'+sharp, x1, y1 - 3)
                        break
                elif bass[1][i] - space - averageLocation - 1 <= y1 <= bass[1][i] - space + averageLocation:
                    if i == 0:
                        displayText(sheet, 'B'+sharp, x1, y1 - 1)
                        break