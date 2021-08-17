import math
from pyproj import Transformer

def roundFloatList(floatList):
    for i in range(0, len(floatList)):
        floatList[i][0] = int(math.ceil(floatList[i][0]))
        floatList[i][1] = int(math.ceil(floatList[i][1]))
    return floatList


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


def stringToFloatList(inputString):
    li = list(inputString.split(","))
    for i in range(len(li)):
        li[i] = float(li[i])
    return li


def listToString(list):
    coordinates = ""
    for elem in list:
        coordinates += str(elem)
        coordinates += ','
    coordinates = coordinates[:-1]
    return coordinates


def arrayToArrayOfPairs(coordinatesArray):
    coordinatesPairArray = []
    for i in range(0, len(coordinatesArray), 2):
        pair = [coordinatesArray[i], coordinatesArray[i + 1]]
        coordinatesPairArray.append(pair)
    return coordinatesPairArray


def verifyOrderOfBboxCoordinates(bbox):
    if type(bbox) == str:
        bbox = stringToFloatList(bbox)
    if bbox[0] > bbox[2]:
        bbox[0], bbox[2] = bbox[2], bbox[0]
    if bbox[1] > bbox[3]:
        bbox[1], bbox[3] = bbox[3], bbox[1]
    return bbox


def epsg3857ToEpsg4326(coordinatesList):
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


def epsg4326ToEpsg3857(coordinatesList):
    newCoordinatesList = []
    # transformer = Transformer.from_crs("epsg:3857", "epsg:4326")
    transformer = Transformer.from_crs("epsg:4326", "epsg:3857", always_xy=True)
    for i in range(0, len(coordinatesList), 2):
        x = coordinatesList[i]
        y = coordinatesList[i + 1]
        x2, y2 = transformer.transform(x, y)
        pair = (x2, y2)
        newCoordinatesList.append(x2)
        newCoordinatesList.append(y2)
    return newCoordinatesList


def getBBOXFromParcelCoordinates(coordinatesList):

    coordinatesBBOX = []
    xList = coordinatesList[0::2]
    yList = coordinatesList[1::2]
    coordinatesBBOXMinX = min(xList)
    coordinatesBBOXMinY = min(yList)
    coordinatesBBOXMaxX = max(xList)
    coordinatesBBOXMaxY = max(yList)
    coordinatesBBOX.append(coordinatesBBOXMinX)
    coordinatesBBOX.append(coordinatesBBOXMinY)
    coordinatesBBOX.append(coordinatesBBOXMaxX)
    coordinatesBBOX.append(coordinatesBBOXMaxY)
    #print(coordinatesBBOX)
    coordinatesBBOX = epsg4326ToEpsg3857(coordinatesBBOX)
    return coordinatesBBOX


def mapPointOnImage(bbox, point):
    bbox = epsg3857ToEpsg4326(bbox)


def pixelMapValue(xmax, xorigin, ymax, yorigin, heigth, width):
    xdif = abs(xmax - xorigin)
    # print(xdif)
    ydif = abs(ymax - yorigin)
    # print(ydif)
    pixelValueX = xdif / width
    pixelValueY = ydif / heigth
    values = [pixelValueX, pixelValueY]
    return values


def mapPolygonPointsOnImage(bbox, polygonCoordinates, heigth, width):
    bbox = verifyOrderOfBboxCoordinates(bbox)
    bbox = epsg3857ToEpsg4326(bbox)
    bboxPoint1 = [bbox[0], bbox[1]]
    bboxPoint2 = [bbox[2], bbox[3]]
    originPoint = [bbox[0], bbox[3]]
    pixelPositions = []
    values = pixelMapValue(bbox[0], bbox[2], bbox[1], bbox[3], heigth, width)
    for i in range(0, len(polygonCoordinates), 2):
        pixelposx = abs(polygonCoordinates[i] - originPoint[0]) / values[0]
        pixelposy = abs(polygonCoordinates[i + 1] - originPoint[1]) / values[1]
        pair = [pixelposx, pixelposy]
        pixelPositions.append(pair)
    return pixelPositions

def pixelsIndicesToCoordinates(pixelIndices, heigth, width, bbox):
    bbox = epsg3857ToEpsg4326(bbox)
    values = pixelMapValue(bbox[0], bbox[2], bbox[1], bbox[3], heigth, width)
    mapCoordinates = []
    originPoint = [bbox[0], bbox[3]]
    for i in range(0, len(pixelIndices)):
        pixelPosX = originPoint[0] + pixelIndices[i][0] * values[0]
        pixelPosY = originPoint[1] + pixelIndices[i][1] * values[1]
        
        # inverted order
        pair = [pixelPosY, pixelPosX]
        #pair = [pixelPosX, pixelPosY]
        mapCoordinates.append(pair)
    return mapCoordinates
