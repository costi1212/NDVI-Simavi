import cv2
import numpy as np

def extractPolygonCorners(imagePath, color):
    img = cv2.imread(imagePath)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = np.float32(hsv)
    if color.upper() == "GREEN":
        hsv = cv2.inRange(hsv, (41, 25, 25), (70, 255, 255))
    elif color.upper() == "YELLOW":
        hsv = cv2.inRange(hsv, (23, 25, 25), (40, 255, 255))
    elif color.upper() == "BROWN":
        hsv = cv2.inRange(hsv, (13, 25, 25), (22, 255, 255))
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = np.float32(gray)
    dst = cv2.cornerHarris(hsv, 5, 3, 0.04)
    ret, dst = cv2.threshold(dst, 0.1 * dst.max(), 255, 0)
    dst = np.uint8(dst)
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(hsv, np.float32(centroids), (5, 5), (-1, -1), criteria)
   # print("Corners "+imagePath + '\n')
    #for i in range(1, len(corners)):
     #   print(corners[i])
    img[dst > 0.1 * dst.max()] = [0, 0, 255]
    cv2.imshow('corners', img)
    #cv2.waitKey(0)
    cv2.imwrite(f'Imagini/{color}points.png', img)
    return corners
    

imagePath = 'Imagini/yellow.png'
image=cv2.imread(imagePath)
cv2.imshow('input image',image)
#cv2.waitKey(0)

gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edged=cv2.Canny(gray,30,200)
cv2.imshow('canny edges',edged)
#cv2.waitKey(0)

contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
#cv2.imshow('canny edges after contouring', edged)
#cv2.waitKey(0)

print(contours)
print('Numbers of contours found=' + str(len(contours)))

corners = extractPolygonCorners(imagePath, "yellow")
#print(corners)

roundedCorners = np.rint(corners)
#print(roundedCorners)
# corner finder
'''
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.

image[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('dst',image)
cv2.waitKey(0)

#print(image[dst>0.01*dst.max()])
'''

#'''
cv2.drawContours(image,contours,-1,(255,0,255),3)
cv2.imshow('contours',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#'''
