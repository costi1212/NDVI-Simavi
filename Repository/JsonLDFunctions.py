import json
import uuid

def createJsonLD(polygonList):

    mainJsonLD = {}
    
    agriParcelRecordJson = createAgriParcelRecordJsonLD()

    graph = []
    mgmtZoneIdList = []
    for poly in polygonList:
        mgmtZoneJson = createManagementZoneJsonLD(poly)
        geomJson = createGeomJsonLD(poly)
        mgmtZoneJson["hasGeometry"] = geomJson["@id"]
        mgmtZoneIdList.append(mgmtZoneJson["@id"])
        graph.append(mgmtZoneJson)
        graph.append(geomJson)

    # remove
    agriParcelRecordJson["containsZone"] = mgmtZoneIdList
    graph.append(agriParcelRecordJson)
    
    mainJsonLD["graph"] = graph
    mainJsonLD["@context"] = "https://w3id.org/demeter/agri-context.jsonld"

    return json.dumps(mainJsonLD)


# Creates a python dictionary with the common fields of all
# JSON entries (id and type).
def createSimpleDictionary(id, type):
    simpleDict = {"@id": id + str(uuid.uuid4()), "@type": type}
    return simpleDict


def createAgriParcelRecordJsonLD():
    
    # de primit prin request
    agriParcelRecordJson = createSimpleDictionary("urn:demeter:AgriParcelRecord:", "AgriParcelRecord")

    # de primit prin request
    agriParcelRecordJson["hasAgriParcel"] = "urn:demeter:AgriParcel:" + str(uuid.uuid4())
    
    return agriParcelRecordJson


def createManagementZoneJsonLD(polygon):
    mgmtZoneJson = createSimpleDictionary("urn:demeter:MgmtZone:", "ManagementZone")
    
    mgmtZoneJson["code"] = polygon.code
    mgmtZoneJson["area"] = polygon.area

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
