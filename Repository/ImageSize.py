from Repository.Conversions import *
from Properties.Properties import *


def getOxDistance(polygonCoordinates):
    coordinates = getBBOXFromParcelCoordinates(polygonCoordinates)
    coordinates = epsg3857ToEpsg4326(coordinates)
    coordinates[2] = coordinates[0]
    return getDistanceFromLatLonInM(coordinates[0], coordinates[1],
                                    coordinates[2], coordinates[3])


def getOyDistance(polygonCoordinates):
    coordinates = getBBOXFromParcelCoordinates(polygonCoordinates)
    coordinates = epsg3857ToEpsg4326(coordinates)
    coordinates[3] = coordinates[1]
    return getDistanceFromLatLonInM(coordinates[0], coordinates[1],
                                    coordinates[2], coordinates[3])


def getWidth(OxDistance):
    return int(OxDistance / 10)


def getHeight(OyDistance):
    return int(OyDistance / 10)


