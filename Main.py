import requests
#import PyLd
from PIL import Image
import io


from Repository.Conversions import mapPolygonPointsOnImage, convertCoordinates, verifyOrderOfBboxCoordinates, \
    listToString, convertNumpyToList
from Repository.ImageEditing import cropImage, colorMask
from Repository.PolygonPoints import loadImage, findContours, extractPolygonCorners, extractPolygons, \
    drawPolygonsAndContours


def requestImage(date, bbox):
    url = f'https://services.terrascope.be/wms/v2?service=WMS&version=1.3.0&request=GetMap&layers=CGS_S2_NDVI&format=image/png&time={date}&width=250&height=250&bbox={bbox}&srs=EPSG:3857'
    response = requests.get(url)
    return response.content


def main():
    #np.set_printoptions(threshold=sys.maxsize)
    polygonCoordinates = [27.199243, 45.910026, 27.209468, 45.911885, 27.209607, 45.906525, 27.200563, 45.904793]
    coordinatesBBOX = [3028959.60, 5766239.96, 3027805.88, 5765105.34]
    pixels = mapPolygonPointsOnImage(coordinatesBBOX, polygonCoordinates, 250, 250)
    coordinatesBBOX = verifyOrderOfBboxCoordinates(coordinatesBBOX)
    responseGet = requestImage('2021-05-15', listToString(coordinatesBBOX))
    bytes = bytearray(responseGet)
    image = Image.open(io.BytesIO(bytes))
    image.save('Imagini\Imagine.png')
    cropImage("Imagini/Imagine.png", pixels)
    colorMask("Imagini/dst.png", "green")
    colorMask("Imagini/dst.png", "yellow")
    colorMask("Imagini/dst.png", "brown")
    image = loadImage('Imagini/yellow.png')
    contours = findContours(image)
    corners = extractPolygonCorners('Imagini/yellow.png', "yellow")
    convertedContours = convertNumpyToList(contours)
    polygons = extractPolygons(convertedContours, corners)
    drawPolygonsAndContours(polygons, contours, image)

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
