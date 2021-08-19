import io
import requests
from numpy.lib.polynomial import poly
from PIL import Image
from Polygon import Polygon
from Properties.Properties import *
from Repository.Conversions import *
from Repository.ImageEditing import *
from Repository.PolygonPoints import *
from Repository.ImageSize import *
from Repository.JsonLDFunctions import createJsonLD
from Repository.JsonFunctions import createJson


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


# Returns a list of Polygon objects.
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
    print("start main")
    width = getWidth(getOxDistance(polygonCoordinates))
    height = getHeight(getOyDistance(polygonCoordinates))
    dataProcessing(polygonCoordinates, date, height, width)
    print("data processed")

    createColorMasks()
    outputJsonLd = open("JsonOutputs/PSDClassification.jsonld", 'w')
    outputJson = open("JsonOutputs/PSDClassification.json", 'w')
    polygonList = []
    
    for i in colors:
        polygonList += getPolygons(i, coordinatesBBOX, height, width)
    
    print("polygons extracted")

    jsonLD = createJsonLD(polygonList)
    outputJsonLd.write(jsonLD)
    print("json-ld output done")

    json = createJson(polygonList)
    outputJson.write(json)
    print("json output done")

    print("done")


if __name__ == '__main__':
    main()