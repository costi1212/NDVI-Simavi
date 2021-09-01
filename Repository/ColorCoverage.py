from PIL import Image
from Properties.Properties import *


# Metoda care numara pxelii care nu sunt negrii dintr-o imagine
# Pe imaginile pe care lucram trebuie sa fie deja aplicata o masca pentru culoarea pe care dorim sa o analizam peste un fundal negru
def countNumberOfPixels(imageNames):
    pixelsdict = {}
    for name in imageNames:
        pixelsdict[name] = 0
        im = Image.open(f'Imagini/{name}.png')
        print(im)
        for pixel in im.getdata():
            if pixel != (0, 0, 0):
                pixelsdict[name] += 1
    for key in pixelsdict:
        pixelsdict[key] /= pixelsdict[croppedImageBlackBackgroundName]
    return pixelsdict





