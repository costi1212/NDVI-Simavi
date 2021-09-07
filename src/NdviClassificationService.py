from flask import Flask, request
from flask_restx import Api, Resource, fields
import io
from Polygon import Polygon
from auxiliaries.ImageSize import *
from auxiliaries.ImageEditing import *
from auxiliaries.JsonLDFunctions import *
from auxiliaries.PolygonPoints import *
from auxiliaries.ImageDate import *
from auxiliaries.ColorCoverage import *
from PIL import Image
from src.Properties import *
from src.auxiliaries.Conversions import *
from src.auxiliaries.JsonFunctions import *


def requestImage(imageDate, bbox, height, width):
    urlRequest = url + defaultArguments + f'&time={imageDate}' + f'&bbox={bbox}' + f'&height={height}' + f'&width={width}'
    print(urlRequest)
    response = requests.get(urlRequest)
    # poate sa adaugam un
    # if response.status_code == 200:
    #   return response.content
    return response.content


def dataProcessing(coordinatesBBOX, polygonCoordinates, dateImage, height, width):
    polygonCoordinatesFloatList = stringToFloatList(polygonCoordinates)
    pixels = mapPolygonPointsOnImage(coordinatesBBOX, polygonCoordinatesFloatList, height, width)
    coordinatesBBOX = verifyOrderOfBboxCoordinates(coordinatesBBOX)
    responseGet = requestImage(dateImage, listToString(coordinatesBBOX), height, width)
    bytes = bytearray(responseGet)
    image = Image.open(io.BytesIO(bytes))
    image.save(imageLocation)
    cropImage(imageLocation, pixels)


def createColorMasks():
    for i in colors:
        colorMask(croppedImageBlackBackground, i)


def getPolygons(color, coordinatesBBOX, height, width):
    path = "resources/images/" + color + ".png"
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
        p = Polygon(coords, colorCode[color.lower()])
        polygonList.append(p)

    return polygonList


flask_app = Flask('NDVIClassification')
app = Api(app=flask_app,
          version='1.0',
          title='NDVI classification',
          description='Classify Images by the NDVI index')

name_space = app.namespace('ndvi', description='NDVI-specific API s')
model = app.model('Input_Json_Model',
                  {
                      'polygonCoordinates': fields.String(
                          required=True,
                          description='Coordinates of the polygon to be analysed.',
                          help='Coordinates cannot be left unspecified.',
                          example=polygonCoordinatesString
                      )
                  })


@name_space.route("/api/json/v1/ndvi-classification")
class JsonApi(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @app.expect(model)
    # @app.marshal_with(model)
    def post(self):
        args = request.json
        print(args)
        coordinatesBBOX = getBBOXFromParcelCoordinates(stringToFloatList(args['polygonCoordinates']))
        width = getWidth(getOxDistance(coordinatesBBOX))
        height = getHeight(getOyDistance(coordinatesBBOX))
        optimalImage = getOptimalDate(args['polygonCoordinates'])
        dataProcessing(coordinatesBBOX, args['polygonCoordinates'], optimalImage[0], height, width)
        createColorMasks()
        polygonList = []
        for i in colors:
            polygonList += getPolygons(i, coordinatesBBOX, height, width)
        imagesForDict = colors[:]
        imagesForDict.append(croppedImageBlackBackgroundName)
        coveragesDict = getCoveragesDict(imagesForDict)
        coveragesDict = createFinalDict(coveragesDict)
        jsonOut = createJson(polygonList, coveragesDict)
        return jsonOut


@name_space.route("/api/jsonld/v1/ndvi-classification")
class JsonldApi(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @app.expect(model)
    def post(self):
        args = request.json
        coordinatesBBOX = getBBOXFromParcelCoordinates(stringToFloatList(args['polygonCoordinates']))
        width = getWidth(getOxDistance(coordinatesBBOX))
        height = getHeight(getOyDistance(coordinatesBBOX))
        optimalImage = getOptimalDate(args['polygonCoordinates'])
        dataProcessing(coordinatesBBOX, args['polygonCoordinates'], optimalImage[0], height, width)
        print(colors)
        createColorMasks()
        polygonList = []
        for i in colors:
            polygonList += getPolygons(i, coordinatesBBOX, height, width)
        imagesForDict = colors[:]
        imagesForDict.append(croppedImageBlackBackgroundName)
        coveragesDict = getCoveragesDict(imagesForDict)
        coveragesDict = createFinalDict(coveragesDict)
        jsonld = createJsonLD(polygonList, coveragesDict)
        return jsonld


flask_app.run(host='0.0.0.0')
