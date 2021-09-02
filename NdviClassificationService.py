from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, fields, marshal_with
from PIL import Image
import io
import requests
import ast
import json

from Main import calculateArea
from Polygon import Polygon
from Repository.Conversions import *
from Repository.ImageSize import *
from Repository.ImageEditing import *
from Properties.Properties import *
from Repository.JsonFunctions import *
from Repository.JsonLDFunctions import *
from Repository.PolygonPoints import *
from Repository.Conversions import mapPolygonPointsOnImage, verifyOrderOfBboxCoordinates
from Repository.ImageDate import *
from Repository.ColorCoverage import *
from flask_apispec import marshal_with
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from flask_apispec.extension import FlaskApiSpec


def requestImage(imageDate, bbox, height, width):
    urlRequest = url + defaultArguments + f'&time={imageDate}' + f'&bbox={bbox}' + f'&height={height}' + f'&width={width}'
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
        p = Polygon(coords, colorCode[color.lower()])
        polygonList.append(p)

    return polygonList


app = Flask('NDVIClassification')
api = Api(app)
app.config["DEBUG"] = True

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='NDVI Classification Service',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})

class APIResponseSchema(Schema):
    ceva = fields.Str(default='Success')

class JsonApi(MethodResource, Resource):
    @marshal_with(APIResponseSchema)
    def post(self):
        args = request.json
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
        jsonOut = createJson(polygonList, coveragesDict)
        return jsonOut


class JsonldApi(Resource):
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
        jsonld = createJsonLD(polygonList, coveragesDict)
        return jsonld


api.add_resource(JsonApi, '/api/json/v1/ndvi-classification')
api.add_resource(JsonldApi, '/api/jsonld/v1/ndvi-classification')
docs = FlaskApiSpec(app)
docs.register(JsonApi)
#docs.register(JsonldApi)
'''

@app.route('/')
def viezureHome():
    return "<h1>Service Documention</h1><p>Information to be added later.</p>"


@app.route('/api/json/v1/ndvi-classification', methods=['POST'])
def getNDVIClassificationAsJson():
    args = request.json
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
    json = createJson(polygonList, coveragesDict)
    return json


@app.route('/api/jsonld/v1/ndvi-classification', methods=['POST'])
def getNDVIClassificationAsJsonLD():
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
    jsonld = createJsonLD(polygonList, coveragesDict)
    return jsonld
'''

app.run()
