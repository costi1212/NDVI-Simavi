from Repository.JsonFunctions import createJson
from numpy.lib.polynomial import poly
from Polygon import Polygon
from Repository.JsonLDFunctions import createJsonLD
import requests
# import PyLd
from PIL import Image
import io
from Properties.Properties import *
from Repository.Conversions import *
from Repository.ImageEditing import *
from Repository.PolygonPoints import *
from shapely.geometry import Polygon as pg
from Repository.ImageSize import *

# Calculates the area by using the property of Shapely's Polygon object
def calculateArea(coordsList):

    x = []
    y = []
    for coords in coordsList:
        x.append(coords[0])
        y.append(coords[1])
    
    pgon = pg(zip(x, y))
    
    return pgon.area * 100 #fiecare pixel are 10 X 10 m2?
    #return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1))) * 100


def requestImage(imageDate, bbox, height, width):
    urlRequest = url + defaultArguments + f'&time={imageDate}' + f'&bbox={bbox}'+f'&height={height}'+f'&width={width}'
    response = requests.get(urlRequest)
    # poate sa adaugam un
    # if response.status_code == 200:
    #   return response.content
    return response.content

# Processing the data and croping the image.
def dataProcessing(polygonCoordinates, dateImage, height, width):
    coordinatesBBOX = getBBOXFromParcelCoordinates(polygonCoordinates)
    pixels = mapPolygonPointsOnImage(coordinatesBBOX, polygonCoordinates, height, width)
    coordinatesBBOX = verifyOrderOfBboxCoordinates(coordinatesBBOX)
    responseGet = requestImage(dateImage, listToString(coordinatesBBOX), height, width)
    bytes = bytearray(responseGet)
    image = Image.open(io.BytesIO(bytes))
    image.save(imageLocation)
    cropImage(imageLocation, pixels)
    return coordinatesBBOX

def getPolygons(color, coordinatesBBOX, height, width):
    path = "Imagini/" + color + ".png"
    image = loadImage(path)
    contours = findContours(image)
    corners = extractPolygonCorners(path, color)
    convertedContours = convertNumpyToList(contours)
    polygonCoords = extractPolygons(convertedContours, corners)

    # Optional step for visualising the results
    drawPolygonsAndContours(polygonCoords, contours, image)

    # Dictionary used to convert color names to the coresponding codes.
    colorCode = {"brown": 0, "yellow": 1, "green": 2}
    polygonList = []
    for poly in polygonCoords:

        # Candidates that have less than 3 points cannot be polygons.
        if len(poly) < 3:
            continue

        coords = pixelsIndicesToCoordinates(poly, height, width, coordinatesBBOX)
        area = calculateArea(poly)
        p = Polygon(coords, colorCode[color.lower()], area)
        polygonList.append(p)

    return polygonList

# Segments the image on 3 colors.
def createColorMasks():
    for i in colors:
        colorMask(croppedImageBlackBackground, i)





def main():
    # np.set_printoptions(threshold=sys.maxsize)
    # data set (should come from REST later on)
    width = getWidth(getOxDistance(polygonCoordinates))
    height = getHeight(getOyDistance(polygonCoordinates))
    dataProcessing(polygonCoordinates, date, height, width)
    createColorMasks()
    outputJsonLd = open("JsonOutputs/PSDClassification.jsonld", 'w')
    outputJson = open("JsonOutputs/PSDClassification.json", 'w')
    polygonList = []
    
    for i in colors:
        polygonList += getPolygons(i, coordinatesBBOX, height, width)
    
    jsonLD = createJsonLD(polygonList)
    outputJsonLd.write(jsonLD)

    json = createJson(polygonList)
    outputJson.write(json)
    
    print("done")


if __name__ == '__main__':
    main()