import json


def createJson(polygonList):

    mainJson = {}

    #mainJson["statistics"] = 
    mainJson["map"] = createMapJson(polygonList)
    
    return json.dumps(mainJson)


def createMapJson(polygonList):

    mapJson = {"type":"FeatureCollection"}

    featureList = []
    for i in range(len(polygonList)):
        featureList.append(createFeatureJson(i, polygonList[i]))
    
    mapJson["features"] = featureList

    #mapJson["crs"] = createCrsJson()

    return mapJson


def createFeatureJson(id, polygon):

    featureJson = {"id":id, "type":"Feature"}
    
    featureJson["properties"] = {"area":polygon.area, "classnr":polygon.code}

    featureJson["geometry"] = {"type":"Polygon", "coordinates":polygon.coords}

    #featureJson["bbox"] = 

    return featureJson
    