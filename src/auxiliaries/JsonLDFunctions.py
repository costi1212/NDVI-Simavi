import uuid
from auxiliaries.JsonFunctions import *

def createJsonLD(polygonList, coveragesDict):

    mainJsonLD = {}

    graph = []
    for poly in polygonList:
        mgmtZoneJson = createManagementZoneJsonLD(poly)
        geomJson = createGeomJsonLD(poly)
        mgmtZoneJson["hasGeometry"] = geomJson["@id"]
        graph.append(mgmtZoneJson)
        graph.append(geomJson)
    
    coveragesDict.pop("dst")
    for color in coveragesDict:
        colorJson = createNdviClassification(color, coveragesDict)
        graph.append(colorJson)

    mainJsonLD["@graph"] = graph
    mainJsonLD["@context"] = "https://w3id.org/demeter/agri-context.jsonld"
    
    return jsonify(mainJsonLD)


# Creates a python dictionary with the common fields of all
# JSON entries (id and type).
def createSimpleDictionary(id, type):
    simpleDict = {"@id": id + str(uuid.uuid4()), "@type": type}
    return simpleDict


def createManagementZoneJsonLD(polygon):
    
    mgmtZoneJson = createSimpleDictionary("urn:demeter:MgmtZone:", "ManagementZone")
    mgmtZoneJson["code"] = polygon.code

    return mgmtZoneJson


def createGeomJsonLD(polygon):

    geomJson = createSimpleDictionary("urn:demeter:MgmtZone:Geom:", "POLYGON")
    coordsString = "POLYGON (("
    
    for coords in polygon.coords:
        coordsString += str(coords[0]) + " " + str(coords[1])+ ", "

    coordsString = coordsString[:-2]
    coordsString += "))"
    geomJson["asWKT"] = coordsString

    return geomJson


def createNdviClassification(colorName, coveragesDict):
    
    colorCodes = {"covered":-1, "brown":0, "yellow":1, "green":2}

    colorJson = createSimpleDictionary("urn:demeter:NdviClassification:", "NdviClassification")
    colorJson["code"] = colorCodes[colorName]
    colorJson["coverage"] = coveragesDict[colorName]

    return colorJson