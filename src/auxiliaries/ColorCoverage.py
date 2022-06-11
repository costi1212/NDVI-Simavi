from PIL import Image
import logging

# Metoda care numara pxelii care nu sunt negrii dintr-o imagine
# Pe imaginile pe care lucram trebuie sa fie deja aplicata o masca pentru culoarea pe care dorim sa o analizam peste un fundal negru
from Properties import *


def getCoveragesDict(imageNames):
    logging.info("Started calculating color coverages")
    pixelsdict = {}
    for name in imageNames:
        pixelsdict[name] = 0
        im = Image.open(f'resources/images/{name}.png')
        for pixel in im.getdata():
            if pixel != (0, 0, 0):
                pixelsdict[name] += 1
    for key in pixelsdict:
        pixelsdict[key] /= pixelsdict[croppedImageBlackBackgroundName]
    logging.info("Finished calculating color coverages")
    return pixelsdict

def getCoveredPixels(whiteBacgroundMask):
    logging.info("Started searching for cloud-covered pixels and counting total pixels")
    coveredPixels = 0
    totalPixels = 1
    im = Image.open(f'resources/images/{whiteBacgroundMask}.png')
    for pixel in im.getdata():
        if pixel != (255, 255, 255):
            totalPixels += 1
            if pixel == (0, 0, 0):
                coveredPixels += 1

    logging.info("Covered pixels found, total pixels counted")
    return coveredPixels/totalPixels


def getTotalPixels(whiteBackgroundMask):

    totalPixels = 0
    im = Image.open(f'resources/images/{whiteBackgroundMask}.png')
    for pixel in im.getdata():
        if pixel != (0, 0, 0):
            totalPixels += 1
    return totalPixels


def createFinalDict(coveragesDict):
    coveragesDict['covered'] = getCoveredPixels(croppedImageWhiteBackgroundName)
    return coveragesDict



