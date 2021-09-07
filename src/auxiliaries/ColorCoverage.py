from PIL import Image
from Properties import *


# Metoda care numara pxelii care nu sunt negrii dintr-o imagine
# Pe imaginile pe care lucram trebuie sa fie deja aplicata o masca pentru culoarea pe care dorim sa o analizam peste un fundal negru
def getCoveragesDict(imageNames):
    pixelsdict = {}
    for name in imageNames:
        pixelsdict[name] = 0
        im = Image.open(f'src/resources/images/{name}.png')
        for pixel in im.getdata():
            if pixel != (0, 0, 0):
                pixelsdict[name] += 1
    for key in pixelsdict:
        pixelsdict[key] /= pixelsdict[croppedImageBlackBackgroundName]
    return pixelsdict

def getCoveredPixels(whiteBacgroundMask):
    coveredPixels = 0
    im = Image.open(f'src/resources/images/{whiteBacgroundMask}.png')
    for pixel in im.getdata():
        if pixel == (0, 0, 0):
            coveredPixels += 1
    return coveredPixels


def getTotalPixels(whiteBacgroundMask):
    totalPixels = 0
    im = Image.open(f'src/resources/images/{whiteBacgroundMask}.png')
    for pixel in im.getdata():
        if pixel != (0, 0, 0):
            totalPixels += 1
    return totalPixels


def createFinalDict(coveragesDict):
    coveragesDict['covered'] = getCoveredPixels(croppedImageWhiteBackgroundName)/getTotalPixels(croppedImageWhiteBackgroundName)
    return coveragesDict



