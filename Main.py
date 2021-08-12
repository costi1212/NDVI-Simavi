from Repository.JsonFunctions import createParcelRecordJson
import requests
#import PyLd
from PIL import Image
import io


from Repository.Conversions import *
from Repository.ImageEditing import *
from Repository.PolygonPoints import *

HEIGHT = 250
WIDTH = 250

def requestImage(date, bbox):
    url = f'https://services.terrascope.be/wms/v2?service=WMS&version=1.3.0&request=GetMap&layers=CGS_S2_NDVI&format=image/png&time={date}&width=250&height=250&bbox={bbox}&srs=EPSG:3857'
    response = requests.get(url)

    # poate sa adaugam un 
    # if response.status_code == 200:
    #   return response.content

    return response.content

# Processing the data and croping the image.
def dataProcessing(coordinatesBBOX, polygonCoordinates):
    pixels = mapPolygonPointsOnImage(coordinatesBBOX, polygonCoordinates, HEIGHT, WIDTH)
    coordinatesBBOX = verifyOrderOfBboxCoordinates(coordinatesBBOX)
    responseGet = requestImage('2021-05-15', listToString(coordinatesBBOX))
    bytes = bytearray(responseGet)
    image = Image.open(io.BytesIO(bytes))
    image.save('Imagini/Imagine.png')
    cropImage("Imagini/Imagine.png", pixels)


# Segments the image on 3 colors.
def createColorMasks():
    colorMask("Imagini/dst.png", "green")
    colorMask("Imagini/dst.png", "yellow")
    colorMask("Imagini/dst.png", "brown")


def getPolygons(color, coordinatesBBOX):

    path = "Imagini/" + color + ".png"
    image = loadImage(path)
    contours = findContours(image)
    corners = extractPolygonCorners(path, color)
    convertedContours = convertNumpyToList(contours)
    polygons = extractPolygons(convertedContours, corners)
    
    # Optional step for visualising the results
    drawPolygonsAndContours(polygons, contours, image)

    polygonsCoords = []
    for poly in polygons:
        coords = pixelsIndicesToCoordinates(poly, HEIGHT, WIDTH, coordinatesBBOX)
        polygonsCoords.append(coords)

    return polygonsCoords


def main():
    #np.set_printoptions(threshold=sys.maxsize)
    #data set (should come from REST later on)
    polygonCoordinates = [27.199243, 45.910026, 27.209468, 45.911885, 27.209607, 45.906525, 27.200563, 45.904793]
    coordinatesBBOX = [3028959.60, 5766239.96, 3027805.88, 5765105.34]

    dataProcessing(coordinatesBBOX, polygonCoordinates)
    createColorMasks()

    greenPolygons = getPolygons("green", coordinatesBBOX)
    yellowPolygons = getPolygons("yellow", coordinatesBBOX)
    brownPolygons = getPolygons("brown", coordinatesBBOX)

    greenJson = createParcelRecordJson(greenPolygons)
    yellowJson = createParcelRecordJson(yellowPolygons)
    brownJson = createParcelRecordJson(brownPolygons)
    
    #print(greenJson)

    #'''

if __name__ == '__main__':
    main()

# de luat imaginea cu 81 81 si testat
# https://services.terrascope.be/wms/v2?service=WMS&version=1.3.0&request=GetMap&layers=CGS_S2_NDVI&format=image/png&time=2021-07-14&bbox=3027805.88,5765105.34,3028959.60,5766239.96&srs=EPSG:3857&styles=&width=81&height=80

# print(convertCoordinates(coordinatesBBOX))
# print(pixelMapValue(converted[0], converted[2], converted[1], converted[3], 250, 250))


# Transform the data from the request into .png

# print(listToString(coordinatesBBOX))

# print(image)


# R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
# A = img[:, :, 3]

# print(R, G, B)
# print(A)

# plotGrayByGreen = 0.9999 * G

# plotGrayByRed = 0.9999 * R

# plotGray = 0.2989 * R + 0.5870 * G + 0.1140 * B
# fig = Figure()

# array = np.zeros([250, 250], dtype=np.uint8)
# ornersGreen=[]

'''
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
'''

# pixelsGreen = extractPolygonCorners("Imagini/green.png", 'green')
# pixelsYellow = extractPolygonCorners("Imagini/yellow.png", 'yellow')
# pixelsBrown = extractPolygonCorners("Imagini/brown.png", 'brown')

# contoursGreen = getContours("Imagini/green.png", 'green')
# contoursYellow = getContours("Imagini/yellow.png", 'yellow')
# contoursBrown = getContours("Imagini/brown.png", 'brown')


# brownCoordinates = pixelsIndicesToCoordinates(pixelsBrown, 250, 250, coordinatesBBOX)


# print(contoursBrown)

# print(pixelsBrown)
# greenCoordinates = pixelsIndicesToCoordinates(pixelsGreen, 250, 250, coordinatesBBOX)
# brownCoordinates = pixelsIndicesToCoordinates(pixelsBrown, 250, 250, coordinatesBBOX)
# print(greenCoordinates)
# plt.show()
