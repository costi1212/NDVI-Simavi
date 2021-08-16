import json
import uuid

from numpy.lib.polynomial import poly

def createJson(polygonList):

    mainJson = {}
    
    agriParcelRecordJson = createAgriParcelRecordJson()

    graph = []
    mgmtZoneIdList = []
    for poly in polygonList:
        mgmtZoneJson = createManagementZoneJson(poly)
        geomJson = createGeomJson(poly)
        mgmtZoneJson["hasGeometry"] = geomJson["@id"]
        mgmtZoneIdList.append(mgmtZoneJson["@id"])
        graph.append(mgmtZoneJson)
        graph.append(geomJson)

    agriParcelRecordJson["containsZone"] = mgmtZoneIdList
    graph.append(agriParcelRecordJson)
    
    mainJson["graph"] = graph
    mainJson["@context"] = "https://w3id.org/demeter/agri-context.jsonld"

    return json.dumps(mainJson)


# Creates a python dictionary with the common fields of all
# JSON entries (id and type).
def createSimpleDictionary(id, type):
    simpleDict = {"@id": id + str(uuid.uuid4()), "@type": type}
    #simpleDict = {"@id": id, "@type": type}
    return simpleDict


def createAgriParcelRecordJson():
    
    agriParcelRecordJson = createSimpleDictionary("urn:demeter:AgriParcelRecord:", "AgriParcelRecord")

    # de primit prin request?
    agriParcelRecordJson["hasAgriParcel"] = "urn:demeter:AgriParcel:" + str(uuid.uuid4())
    
    return agriParcelRecordJson


def createManagementZoneJson(polygon):
    mgmtZoneJson = createSimpleDictionary("urn:demeter:MgmtZone:", "ManagementZone")
    
    # trebuie sa ajunga culoarea si aria aici
    #mgmtZoneJson["code"] = 
    #mgmtZoneJson["area"] =

    return mgmtZoneJson


def createGeomJson(polygon):

    geomJson = createSimpleDictionary("urn:demeter:MgmtZone:Geom:", "POLYGON")
    
    coordsString = "POLYGON (("
    
    # de rezolvat virgula la final
    for coords in polygon:
        coordsString += str(coords[0]) + " " + str(coords[1])+ ", "

    #coordsString += str(polygon[-1][0]) + " " + str(polygon[-1][1]) + "))"
    #coordsString += str(polygon[-1]) + "))"
    coordsString = coordsString[:-2]
    coordsString += "))"

    geomJson["asWKT"] = coordsString

    return geomJson
