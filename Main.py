import requests
import cv2.cv2 as cv2
import numpy as np
import sys
import pyproj
from pyproj import Transformer
import math
from PIL import Image
import io
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.figure import Figure

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from numpy import asarray
from numpy import savetxt

#masca gaussiana [1 2 1] [2 4 2] [1 2 1]

np.set_printoptions(threshold=sys.maxsize)
#Variabile globale


# Request function
def stringToFloatList(inputString):
    li = list(inputString.split(","))
    [float(i) for i in li]
    return li


def listToString(list):
    coordinates = ""
    for elem in list:
        coordinates += str(elem)
        coordinates += ','
    coordinates = coordinates[:-1]
    return coordinates


def verifyOrderOfBboxCoordinates(bbox):
    if type(bbox) == str:
        bbox = stringToFloatList(bbox)
    if bbox[0] > bbox[2]:
        bbox[0], bbox[2] = bbox[2], bbox[0]
    if bbox[1] > bbox[3]:
        bbox[1], bbox[3] = bbox[3], bbox[1]
    return bbox


def convertCoordinates(coordinatesList):
    newCoordinatesList = []
    # transformer = Transformer.from_crs("epsg:3857", "epsg:4326")
    transformer = Transformer.from_crs("epsg:3857", "epsg:4326", always_xy=True)
    for i in range(0, len(coordinatesList), 2):
        x = coordinatesList[i]
        y = coordinatesList[i + 1]
        x2, y2 = transformer.transform(x, y)
        pair = (x2, y2)
        newCoordinatesList.append(x2)
        newCoordinatesList.append(y2)
    return newCoordinatesList


def pixelMapValue(xmax, xorigin, ymax, yorigin, length, width):
    xdif = abs(xmax - xorigin)
    # print(xdif)
    ydif = abs(ymax - yorigin)
    # print(ydif)
    pixelValueX = xdif / width
    pixelValueY = ydif / length
    values = [pixelValueX, pixelValueY]
    return values


def arrayToArrayOfPairs(coordinatesArray):
    coordinatesPairArray = []
    for i in range(0, len(coordinatesArray), 2):
        pair = [coordinatesArray[i], coordinatesArray[i + 1]]
        coordinatesPairArray.append(pair)
    return coordinatesPairArray


def mapPointOnImage(bbox, point):
    bbox = convertCoordinates(bbox)


def pixelsIndicesToCoordinates(pixelIndices, length, width, bbox):
    bbox = convertCoordinates(bbox)
    values = pixelMapValue(bbox[0], bbox[2], bbox[1], bbox[3], length, width)
    mapCoordinates = []
    originPoint = [bbox[0], bbox[3]]
    for i in range(0, len(pixelIndices)):
        pixelPosX = originPoint[0] + pixelIndices[i][0] * values[0]
        pixelPosY = originPoint[1] + pixelIndices[i][1] * values[1]
        pair = [pixelPosX, pixelPosY]
        mapCoordinates.append(pair)
    return mapCoordinates



def mapPolygonPointsOnImage(bbox, polygonCoordinates, length, width):
    bbox = verifyOrderOfBboxCoordinates(bbox)
    bbox = convertCoordinates(bbox)
    bboxPoint1 = [bbox[0], bbox[1]]
    bboxPoint2 = [bbox[2], bbox[3]]
    originPoint = [bbox[0], bbox[3]]
    pixelPositions = []
    values = pixelMapValue(bbox[0], bbox[2], bbox[1], bbox[3], length, width)
    for i in range(0, len(polygonCoordinates), 2):
        pixelposx = abs(polygonCoordinates[i] - originPoint[0]) / values[0]
        pixelposy = abs(polygonCoordinates[i + 1] - originPoint[1]) / values[1]
        pair = [pixelposx, pixelposy]
        pixelPositions.append(pair)
    return pixelPositions


def roundFloatList(floatList):
    for i in range(0, len(floatList)):
        floatList[i][0] = int(math.ceil(floatList[i][0]))
        floatList[i][1] = int(math.ceil(floatList[i][1]))
    return floatList

def requestImage(date, bbox):
    url = f'https://services.terrascope.be/wms/v2?service=WMS&version=1.3.0&request=GetMap&layers=CGS_S2_NDVI&format=image/png&time={date}&width=250&height=250&bbox={bbox}&srs=EPSG:3857'
    response = requests.get(url)
    return response.content

#def clasifyPixels():





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
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = np.float32(gray)
    dst = cv2.cornerHarris(hsv, 5, 3, 0.04)
    ret, dst = cv2.threshold(dst, 0.1 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(hsv, np.float32(centroids), (5, 5), (-1, -1), criteria)
    print("Corners "+imagePath + '\n')
    for i in range(0, len(corners)):
        print(corners[i])
    img[dst > 0.1 * dst.max()] = [0, 0, 255]
    print("DST:")
    print(dst[dst > 0.1 * dst.max()])
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.imwrite(f'Imagini/{color}points.png', img)
    cv2.destroyAllWindows
    corners1 = corners
    #print(corners1)
    return corners


def colorMask(imagePath, color):
    ## Read
    img = cv2.imread(imagePath)

    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    if color.upper() == "GREEN":
        mask = cv2.inRange(hsv, (41, 25, 25), (70, 255, 255))
    elif color.upper() == "YELLOW":
        mask = cv2.inRange(hsv, (23, 25, 25), (40, 255, 255))
    elif color.upper() == "BROWN":
        mask = cv2.inRange(hsv, (13, 25, 25), (22, 255, 255))

    ## slice the green
    imask = mask > 0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    ## save
    cv2.imwrite(f"Imagini/{color}.png", green)



def cropImage(imagePath, pixelIndicesArray):
    img = cv2.imread(imagePath)
    pixelIndicesArray = roundFloatList(pixelIndicesArray)
    pts = np.array(pixelIndicesArray)
    print(pts)

    #(1) Crop the polygon
    polygon = cv2.boundingRect(pts)
    x, y, w, h = polygon
    croped = img[y: y+h, x:x+w].copy()


    #(2) make mask
    pts = pts - pts.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    #(3) do bit op
    dst = cv2.bitwise_and(croped, croped, mask=mask)

    #(4) add white background
    bg = np.ones_like(croped, np.uint8)*255
    cv2.bitwise_not(bg, bg, mask=mask)
    dst2 = bg + dst

    cv2.imwrite("Imagini/croped.png", croped)
    cv2.imwrite("Imagini/mask.png", mask)
    cv2.imwrite("Imagini/dst.png", dst)
    cv2.imwrite("Imagini/dst2.png", dst2)


def main():
    print("In main")


if __name__ == '__main__':
    main()

polygonCoordinates = [27.199243, 45.910026, 27.209468, 45.911885, 27.209607, 45.906525, 27.200563, 45.904793]
coordinatesBBOX = [3028959.60, 5766239.96, 3027805.88, 5765105.34]


# de luat imaginea cu 81 81 si testat
# https://services.terrascope.be/wms/v2?service=WMS&version=1.3.0&request=GetMap&layers=CGS_S2_NDVI&format=image/png&time=2021-07-14&bbox=3027805.88,5765105.34,3028959.60,5766239.96&srs=EPSG:3857&styles=&width=81&height=80
pixels = mapPolygonPointsOnImage(coordinatesBBOX, polygonCoordinates, 250, 250)

converted = convertCoordinates(coordinatesBBOX)
#print(convertCoordinates(coordinatesBBOX))
#print(pixelMapValue(converted[0], converted[2], converted[1], converted[3], 250, 250))


# Transform the data from the request into .png
coordinatesBBOX = verifyOrderOfBboxCoordinates(coordinatesBBOX)
#print(listToString(coordinatesBBOX))
responseGet = requestImage('2021-05-15', listToString(coordinatesBBOX))
bytes = bytearray(responseGet)
image = Image.open(io.BytesIO(bytes))
print(image)

image.save('Imagini\Imagine.png')
cropImage("Imagini/Imagine.png", pixels)
img = mpimg.imread('Imagini\dst2.png')


R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
#A = img[:, :, 3]

#print(R, G, B)
#print(A)

plotGrayByGreen = 0.9999 * G

plotGrayByRed = 0.9999 * R

plotGray = 0.2989 * R + 0.5870 * G + 0.1140 * B
fig = Figure()

array = np.zeros([250, 250], dtype=np.uint8)
#ornersGreen=[]


plot1 = plt.figure('Normal')
plt.imshow(plotGray, cmap='gray')
plot2 = plt.figure('Green')
plt.imshow(plotGrayByGreen, cmap='gray')
plot3 = plt.figure('Red')
plt.imshow(plotGrayByRed, cmap='gray')
#extractPolygonCorners("Imagini/Imagine.png")
imgGray = cv2.imread('Imagini/dst2.png', 0)
cv2.imwrite("Imagini/Gray.png", imgGray)
#extractPolygonCorners("Imagini/Gray.png")
color = "green"
colorMask("Imagini/dst.png", "green")
colorMask("Imagini/dst.png", "yellow")
colorMask("Imagini/dst.png", "brown")

pixelsGreen = extractPolygonCorners("Imagini/green.png", 'green')
pixelsYellow = extractPolygonCorners("Imagini/yellow.png", 'yellow')
pixelsBrown = extractPolygonCorners("Imagini/brown.png", 'brown')

#print(pixelsBrown)
#greenCoordinates = pixelsIndicesToCoordinates(pixelsGreen, 250, 250, coordinatesBBOX)
brownCoordinates = pixelsIndicesToCoordinates(pixelsBrown, 250, 250, coordinatesBBOX)
print(brownCoordinates)
print(pixelsBrown)
#print(greenCoordinates)
#plt.show()
