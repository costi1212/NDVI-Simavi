import cv2
import numpy as np
from numpy.core.numeric import count_nonzero
import random

def extractPolygonCorners(imagePath, color):
    img = cv2.imread(imagePath)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = np.float32(hsv)
    if color.upper() == "GREEN":
        hsv = cv2.inRange(hsv, (41, 25, 25), (70, 255, 255))
    elif color.upper() == "YELLOW":
        hsv = cv2.inRange(hsv, (23, 25, 25), (40, 255, 255))
    elif color.upper() == "BROWN":
        hsv = cv2.inRange(hsv, (13, 25, 25), (22, 255, 255))

    dst = cv2.cornerHarris(hsv, 5, 3, 0.04)
    _, dst = cv2.threshold(dst, 0.1 * dst.max(), 255, 0)
    #dst = np.uint8(dst)
    img[dst > 0.1 * dst.max()] = [0, 0, 255]
    
    corners = []
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (img[i][j] == [0, 0, 255]).all():
                corners.append([j, i])

    #corners = np.uint8(corners)
    cv2.imshow('corners', img)
    cv2.imwrite(f'Imagini/{color}points.png', img)
    return corners
    

imagePath = 'Imagini/yellow.png'
image=cv2.imread(imagePath)
cv2.imshow('input image',image)

gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edged=cv2.Canny(gray,30,200)

contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

corners = extractPolygonCorners(imagePath, "yellow")

#'''
# PROBLEMA DE COMPARARE INTRE LISTE
# ndarray sau list?
polygons = []
for cont in contours:
    aux = cont.tolist()
    poly = []
    for coords in corners:
        if coords in aux:
            poly.append(coords)

           
        #for c in cont:
        # !functioneaza dar merge foarte greu! 
         #   if (coords == c).all():
          #      poly.append(coords)
        
    polygons.append(poly)

print('Numbers of contours found:' + str(len(contours)))
print("Number of polygons:" + str(len(polygons)))

for p in polygons:
    b = random.randint(0,255)
    r = random.randint(0,255)
    g = random.randint(0,255)
    
    for c in p:
        image[c[1]][c[0]] = [b,g,r]
        

cv2.imshow("polygons", image)
#'''
cv2.drawContours(image,contours,-1,(255,0,255),3) 
cv2.imshow('contours',image)
cv2.waitKey(0)
cv2.destroyAllWindows()