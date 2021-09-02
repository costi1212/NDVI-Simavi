import json

from flask import jsonify


def createJson(polygonList, coveragesDict):
    mainJson = {}
    mainJson["statistics"] = createStatisticsList(coveragesDict)
    mainJson["map"] = createMapJson(polygonList)

    return jsonify(mainJson)


def createMapJson(polygonList):
    mapJson = {"type": "FeatureCollection"}
    featureList = []

    for i in range(len(polygonList)):
        featureList.append(createFeatureJson(i, polygonList[i]))

    mapJson["features"] = featureList
    mapJson["crs"] = {"type": "name", "name": "urn:ogc:def:crs:EPSG::4326"}

    return mapJson


def createFeatureJson(id, polygon):
    featureJson = {"id": id, "type": "Feature"}
    featureJson["properties"] = {"classnr": polygon.code}
    featureJson["geometry"] = {"type": "Polygon", "coordinates": polygon.coords}

    return featureJson


# Takes the color list as parameter (in the non-hardcoded version).
def createStatisticsList(coveragesDict):
    statistics = []

    # This version of the program is hardcoded for 3 colors.
    statsBrown = {"code": 0, "colorHex": "#8A7010", "coverage": coveragesDict["brown"]}
    statsYellow = {"code": 1, "colorHex": "#8A6210", "coverage": coveragesDict["yellow"]}
    statsGreen = {"code": 2, "colorHex": "#768A10", "coverage": coveragesDict["green"]}

    statistics.append(statsBrown)
    statistics.append(statsYellow)
    statistics.append(statsGreen)

    return statistics
