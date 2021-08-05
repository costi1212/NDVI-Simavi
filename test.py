import cv2
import numpy as np



image=cv2.imread('Imagini/yellow.png')
cv2.imshow('input image',image)
cv2.waitKey(0)

gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edged=cv2.Canny(gray,30,200)
cv2.imshow('canny edges',edged)
cv2.waitKey(0)

contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.imshow('canny edges after contouring', edged)
cv2.waitKey(0)

print(contours)
print('Numbers of contours found=' + str(len(contours)))

cv2.drawContours(image,contours,-1,(0,0,255),3)
cv2.imshow('contours',image)
cv2.waitKey(0)
cv2.destroyAllWindows()