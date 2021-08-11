import json
import uuid

# Creates a python dictionary with the common fields of all
# JSON entries (id and type).
def createSimpleDictionary(id, type):

    simpleDict = {"@id":id + str(uuid.uuid4()), "@type":type}

    return simpleDict


def createParcelRecordJson(polygons):

    parcelRecordJson = createSimpleDictionary("urn:demeter:AgriParcelRecord:", "AgriParcelRecord")
    
    #'''
    zoneList = []
    for poly in polygons:
        zone = createManagementZoneJson(poly)
        zoneList.append(zone)

    parcelRecordJson["containsZone"] = zoneList
    #'''
    return json.dumps(parcelRecordJson)


def createManagementZoneJson(polygon):

    mgmtZoneJson = createSimpleDictionary("urn:demeter:MgmtZone:", "ManagementZone")
    hasGeometry = createPolygonJson(polygon)

    mgmtZoneJson["hasGeometry"] = hasGeometry

    return json.dumps(mgmtZoneJson)


def createPolygonJson(polygon):
    
    polygonJson = createSimpleDictionary("urn:demeter:MgmtZone:Geom:", "Polygon")

    # de adaugat coordonatele din polygon[]
    #polygonJson["asWKT"] = 

    return json.dumps(polygonJson)
