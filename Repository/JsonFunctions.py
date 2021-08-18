import json


def createJson(polygonList):
    
    mainJson = {}
    mainJson["statistics"] = createStatisticsList()
    mainJson["map"] = createMapJson(polygonList)
    
    return json.dumps(mainJson)


def createMapJson(polygonList):
    
    mapJson = {"type":"FeatureCollection"}
    featureList = []

    for i in range(len(polygonList)):
        featureList.append(createFeatureJson(i, polygonList[i]))
    
    mapJson["features"] = featureList
    mapJson["crs"] = {"type":"name", "name":"urn:ogc:def:crs:EPSG::4326"}

    return mapJson


def createFeatureJson(id, polygon):

    featureJson = {"id":id, "type":"Feature"}
    featureJson["properties"] = {"area":polygon.area, "classnr":polygon.code}
    featureJson["geometry"] = {"type":"Polygon", "coordinates":polygon.coords}

    return featureJson

# Takes the color list as parameter (in the non-hardcoded version).
def createStatisticsList():

    statistics = []

    # Good version:
    '''
    for i in range(len(colorList)):
        stats = {}
        stats["classnr"] = i
        stats["hex"] = colorList[i]
        statistics.append(stats)
    '''

    # Hardcoded version:
    statsBrown = {"classnr":0, "hex":"#8A7010"}
    statsYellow = {"classnr":1, "hex":"#8A6210"}
    statsGreen = {"classnr":2, "hex":"#768A10"}
    statistics.append(statsBrown)
    statistics.append(statsYellow)
    statistics.append(statsGreen)

    return statistics