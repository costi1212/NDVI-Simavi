from flask import Flask, request, jsonify
from PIL import Image
import io
from flask_restful import Resource, Api, reqparse
import requests
import pandas as pd
import ast

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


def requestImage(imageDate, bbox, height, width):
    urlRequest = url + defaultArguments + f'&time={imageDate}' + f'&bbox={bbox}'+f'&height={height}'+f'&width={width}'
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
        area = calculateArea(poly)
        p = Polygon(coords, colorCode[color.lower()], area)
        polygonList.append(p)

    return polygonList


app = Flask('NDVIClassification')
app.config["DEBUG"] = True


@app.route('/')
def viezureHome():
    return "<h1>Service Documention</h1><p>Information to be added later.</p>"


@app.route('/api/json/v1/ndvi-classification', methods=['POST'])
def getNDVIClassificationAsJson():
    args = request.json
    coordinatesBBOX = getBBOXFromParcelCoordinates(stringToFloatList(args['polygonCoordinates']))
    width = getWidth(getOxDistance(coordinatesBBOX))
    height = getHeight(getOyDistance(coordinatesBBOX))
    dataProcessing(coordinatesBBOX, args['polygonCoordinates'], args['date'], height, width)
    createColorMasks()
    polygonList = []
    for i in colors:
        polygonList += getPolygons(i, coordinatesBBOX, height, width)
    json = createJson(polygonList)
    return json


@app.route('/api/jsonld/v1/ndvi-classification', methods=['POST'])
def getNDVIClassificationAsJsonLD():
    args = request.json
    coordinatesBBOX = getBBOXFromParcelCoordinates(stringToFloatList(args['polygonCoordinates']))
    width = getWidth(getOxDistance(coordinatesBBOX))
    height = getHeight(getOyDistance(coordinatesBBOX))
    dataProcessing(coordinatesBBOX, args['polygonCoordinates'], args['date'], height, width)
    createColorMasks()
    polygonList = []
    for i in colors:
        polygonList += getPolygons(i, coordinatesBBOX, height, width)
    jsonld = createJsonLD(polygonList)
    return jsonld


app.run()
