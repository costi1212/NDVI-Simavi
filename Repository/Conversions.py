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
    [float(i) for i in li]
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


def mapPointOnImage(bbox, point):
    bbox = convertCoordinates(bbox)


def pixelMapValue(xmax, xorigin, ymax, yorigin, length, width):
    xdif = abs(xmax - xorigin)
    # print(xdif)
    ydif = abs(ymax - yorigin)
    # print(ydif)
    pixelValueX = xdif / width
    pixelValueY = ydif / length
    values = [pixelValueX, pixelValueY]
    return values


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