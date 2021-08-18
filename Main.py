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

def requestImage(imageDate, bbox):
    url = f'https://services.terrascope.be/wms/v2?service=WMS&version=1.3.0&request=GetMap&layers=CGS_S2_NDVI&format=image/png&width=250&height=250&srs=EPSG:3857&time={date}&bbox={bbox}'
    response = requests.get(url)
    # poate sa adaugam un 
    # if response.status_code == 200:
    #   return response.content
    return response.content


# Processing the data and croping the image.
def dataProcessing(coordinatesBBOX, polygonCoordinates, imageDate):
    pixels = mapPolygonPointsOnImage(coordinatesBBOX, polygonCoordinates, HEIGHT, WIDTH)
    coordinatesBBOX = verifyOrderOfBboxCoordinates(coordinatesBBOX)
    responseGet = requestImage(imageDate, listToString(coordinatesBBOX))
    bytes = bytearray(responseGet)
    image = Image.open(io.BytesIO(bytes))
    image.save(imageLocation)
    cropImage(imageLocation, pixels)


# Segments the image on 3 colors.
def createColorMasks():
    for i in colors:
        colorMask(croppedImageBlackBackground, i)


# Returns a list of Polygon objects.
def getPolygons(color, coordinatesBBOX):
    path = "Imagini/" + color + ".png"
    image = loadImage(path)
    contours = findContours(image)
    corners = extractPolygonCorners(path, color)
    convertedContours = convertNumpyToList(contours)
    polygonCoords = extractPolygons(convertedContours, corners)

    # Optional step for visualising the results
    #drawPolygonsAndContours(polygonCoords, contours, image)

    # Dictionary used to convert color names to the coresponding codes.
    colorCode = {"brown": 0, "yellow": 1, "green": 2}
    polygonList = []
    for poly in polygonCoords:
        
        # Candidates that have less than 3 points cannot be polygons.
        if len(poly) < 3:
            continue

        coords = pixelsIndicesToCoordinates(poly, HEIGHT, WIDTH, coordinatesBBOX)
        area = calculateArea(poly)
        p = Polygon(coords, colorCode[color.lower()], area)
        polygonList.append(p)

    return polygonList


def main():
    # np.set_printoptions(threshold=sys.maxsize)
    # data set (should come from REST later on)
    dataProcessing(coordinatesBBOX, polygonCoordinates, date)
    createColorMasks()
    
    outputJsonLd = open("JsonOutputs/PSDClassification.jsonld", 'w')
    outputJson = open("JsonOutputs/PSDClassification.json", 'w')
    polygonList = []
    
    for i in colors:
        polygonList += getPolygons(i, coordinatesBBOX)
    
    jsonLD = createJsonLD(polygonList)
    outputJsonLd.write(jsonLD)

    json = createJson(polygonList)
    outputJson.write(json)
    
    print("done")


if __name__ == '__main__':
    main()