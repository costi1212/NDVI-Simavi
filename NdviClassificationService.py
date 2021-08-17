from flask import Flask, request, jsonify
from PIL import Image
import io
from flask_restful import Resource, Api, reqparse
import requests
import pandas as pd
import ast

from Repository.Conversions import *
from Repository.ImageEditing import *
from Properties.Properties import *
from Repository.JsonFunctions import *
from Repository.PolygonPoints import *
from Repository.Conversions import mapPolygonPointsOnImage, verifyOrderOfBboxCoordinates


def requestImage(imageDate, bbox):
    urlRequest = url + defaultArguments + f'&time={imageDate}' + f'&bbox={bbox}'
    response = requests.get(urlRequest)
    # poate sa adaugam un
    # if response.status_code == 200:
    #   return response.content
    return response.content


def dataProcessing(polygonCoordinates, dateImage):
    polygonCoordinatesFloatList = stringToFloatList(polygonCoordinates)
    coordinatesBBOX = getBBOXFromParcelCoordinates(polygonCoordinatesFloatList)
    print(coordinatesBBOX)
    pixels = mapPolygonPointsOnImage(coordinatesBBOX, polygonCoordinatesFloatList, HEIGHT, WIDTH)
    coordinatesBBOX = verifyOrderOfBboxCoordinates(coordinatesBBOX)
    responseGet = requestImage(dateImage, listToString(coordinatesBBOX))
    bytes = bytearray(responseGet)
    image = Image.open(io.BytesIO(bytes))
    image.save(imageLocation)
    cropImage(imageLocation, pixels)
    return coordinatesBBOX


def createColorMasks():
    for i in colors:
        colorMask(croppedImageBlackBackground, i)


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


app = Flask('NDVIClassification')
app.config["DEBUG"] = True


@app.route('/')
def home():
    return "<h1>Service Documention</h1><p>Information to be added later.</p>"


@app.route('/simpleJson', methods=['GET', 'POST'])
def returnSimpleJson():
    args = request.json
    coordinatesBBOX = dataProcessing(args['polygonCoordinates'], args['date'])
    createColorMasks()
    #OutputFile = open(jsonOutputs, 'w')
    outputJson = []
    for i in colors:
        Polygons = getPolygons(i, coordinatesBBOX)
        print(Polygons)
        # ordinea itemilor din json este gresita
        Json = createJson(Polygons)
        outputJson.append(Json)
        # print(Json)
        #OutputFile.write(i.upper())
        #OutputFile.write(Json)
        #OutputFile.write('\n \n \n')
    return jsonify(outputJson)


app.run()
