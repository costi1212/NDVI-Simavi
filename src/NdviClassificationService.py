from flask import Flask, request
from flask_restx import Api, Resource, fields, abort
import io
from werkzeug.exceptions import Unauthorized
from requests import Response

from Polygon import Polygon
from auxiliaries.ImageSize import *
from auxiliaries.ImageEditing import *
from auxiliaries.JsonLDFunctions import *
from auxiliaries.PolygonPoints import *
from auxiliaries.ImageDate import *
from auxiliaries.ColorCoverage import *
from PIL import Image
from Properties import *
from auxiliaries.Conversions import *
from auxiliaries.JsonFunctions import *
import logging
import sys


def requestImage(imageDate, bbox, height, width):
    urlRequest = url + defaultArguments + f'&time={imageDate}' + f'&bbox={bbox}' + f'&height={height}' + f'&width={width}'
    print(urlRequest)
    response = requests.get(urlRequest)
    if response.status_code == 200:
        logging.info("Image retrieved from Terrascope service.")
        return response.content
    else:
        logging.critical("Could not retrieve image from Terrascope service.")
        sys.exit()


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

    logging.info("Image cropped, rescaled and split into sub-images.")


def getPolygons(color, coordinatesBBOX, height, width):
    path = "resources/images/" + color + ".png"

    try:
        image = loadImage(path)
    except:
        logging.exception("Could not read image from relative path " + path)

    contours = findContours(image)
    corners = extractPolygonCorners(path, color)
    convertedContours = convertNumpyToList(contours)
    polygonCoords = extractPolygons(convertedContours, corners)

    # Optional step for visualising the results
    # drawPolygonsAndContours(polygonCoords, contours, image)

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

    logging.info("Polygons extracted from the " + color + " image.")

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
                      ),
                      'clientId': fields.String(
                          required=True,
                          description='Coordinates of the polygon to be analysed.',
                          help='Coordinates cannot be left unspecified.',
                          example=token
                      )
                  })


@name_space.route("/api/json/v1/ndvi-classification")
class JsonApi(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @app.expect(model)
    # @app.marshal_with(model)
    def post(self):
        logging.basicConfig(filename='events.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        args = request.json
        logging.info("Checking token")
        if (args['clientId'] == token):
            logging.info("Token is valid")
            logging.info("Simple Json request started.")

            # print(args)
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
            logging.info("Json generated.")
            logging.info("Simple Json request ended.")
            return jsonOut
        else:
            logging.info("Invalid token!")
            app.abort(401, "Invalid token!")


@name_space.route("/api/jsonld/v1/ndvi-classification")
class JsonldApi(Resource):
    @app.doc(responses={200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
    @app.expect(model)
    def post(self):
        logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                            level=logging.INFO)
        args = request.json
        logging.info("Checking token")
        if (args['clientId'] == token):
            logging.info("Token is valid")
            logging.info("JsonLd request started.")
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
            logging.info("JsonLd generated.")
            logging.info("JsonLd request ended.")
            return jsonld
        else:
            logging.info("Invalid token!")
            app.abort(401, "Invalid token!")


flask_app.run(host='0.0.0.0')
