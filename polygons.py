import cv2
import numpy as np
from numpy.core.numeric import count_nonzero
import random

# Loads the image at the given path.
def loadImage(imagePath):
    image=cv2.imread(imagePath)
    cv2.imshow('input image',image)
    cv2.waitKey(0)
    return image

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
    img[dst > 0.1 * dst.max()] = [0, 0, 255]
    
    corners = []
    for i in range(len(img)):
        for j in range(len(img[0])):
            if (img[i][j] == [0, 0, 255]).all():
                corners.append([j, i])

    cv2.imshow('corners', img)
    cv2.imwrite(f'Imagini/{color}points.png', img)
    return corners


# Finds the contours of all the shapes of the given image.
# The contours are returned as a list of lists.
def findContours(image):
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    edged=cv2.Canny(gray,30,200)
    contours, _ = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    return contours


# Converts a 3 level numpy arrray to a 2 level list.
def convertNumpyToList(nparray):
    aux = []
    newList = []
    for val in nparray:
        aux = []
        for i in val:
            for j in i:
                aux.append(j.tolist())
        newList.append(aux)

    return newList


# Returns a list of corner coordinates for each polygon. 
def extractPolygons(contours, corners):
    polygons = []
    for contour in contours:
        poly = []
        for coords in corners:
            if coords in contour:
                poly.append(coords) 

        polygons.append(poly)

    return polygons

# Auxiliary function for visualising the polygons.
def drawPolygonsAndContours(polygons, contours, image):
    for p in polygons:
        b = random.randint(0,255)
        r = random.randint(0,255)
        g = random.randint(0,255)        
        for c in p:
            cv2.circle(image, (c[0],c[1]), 1, (b,r,g), 1)

    cv2.imshow("polygons", image)
    cv2.drawContours(image,contours,-1,(255,0,255),3) 
    cv2.imshow('contours',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main():
    image = loadImage('Imagini/green.png')
    contours = findContours(image)
    corners = extractPolygonCorners('Imagini/green.png', "green")
    convertedContours = convertNumpyToList(contours)
    polygons = extractPolygons(convertedContours, corners)
    drawPolygonsAndContours(polygons,contours, image)

if __name__ == "__main__":
    main()