from Repository.Conversions import *
from Properties.Properties import *


def getOxDistance(BBOXCoordinates):
    BBOXCoord = epsg3857ToEpsg4326(BBOXCoordinates)
    BBOXCoord[2] = BBOXCoord[0]
    return getDistanceFromLatLonInM(BBOXCoord[1], BBOXCoord[0],
                                    BBOXCoord[3], BBOXCoord[2])


def getOyDistance(BBOXCoordinates):
    BBOXCoord = epsg3857ToEpsg4326(BBOXCoordinates)
    BBOXCoord[3] = BBOXCoord[1]
    return getDistanceFromLatLonInM(BBOXCoord[1], BBOXCoord[0],
                                    BBOXCoord[3], BBOXCoord[2])


def getWidth(OxDistance):
    return int(OxDistance / 10)


def getHeight(OyDistance):
    return int(OyDistance / 10)