import cv2
import numpy as np
from auxiliaries.Conversions import roundFloatList


def cropImage(imagePath, pixelIndicesArray):
    img = cv2.imread(imagePath)
    pixelIndicesArray = roundFloatList(pixelIndicesArray)
    pts = np.array(pixelIndicesArray)

    # (1) Crop the polygon
    polygon = cv2.boundingRect(pts)
    x, y, w, h = polygon
    croped = img[y: y + h, x:x + w].copy()

    # (2) make mask
    pts = pts - pts.min(axis=0)

    mask = np.zeros(croped.shape[:2], np.uint8)
    cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)

    # (3) do bit op
    dst = cv2.bitwise_and(croped, croped, mask=mask)

    # (4) add white background
    bg = np.ones_like(croped, np.uint8) * 255
    cv2.bitwise_not(bg, bg, mask=mask)
    dst2 = bg + dst

    cv2.imwrite("src/resources/images/croped.png", croped)
    cv2.imwrite("src/resources/images/mask.png", mask)
    cv2.imwrite("src/resources/images/dst.png", dst)
    cv2.imwrite("src/resources/images/dst2.png", dst2)


def colorMask(imagePath, color):
    ## Read
    img = cv2.imread(imagePath)

    ## convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## mask of green (36,25,25) ~ (86, 255,255)
    if color.upper() == "GREEN":
        mask = cv2.inRange(hsv, (41, 25, 25), (70, 255, 255))
    elif color.upper() == "YELLOW":
        mask = cv2.inRange(hsv, (23, 25, 25), (40, 255, 255))
    elif color.upper() == "BROWN":
        mask = cv2.inRange(hsv, (13, 25, 25), (22, 255, 255))

    ## slice the green
    imask = mask > 0
    green = np.zeros_like(img, np.uint8)
    green[imask] = img[imask]

    ## save
    cv2.imwrite(f"src/resources/images/{color}.png", green)