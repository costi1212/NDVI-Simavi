import cv2
import numpy as np



image=cv2.imread('Imagini/brown.png')
cv2.imshow('input image',image)
#cv2.waitKey(0)

gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

edged=cv2.Canny(gray,30,200)
cv2.imshow('canny edges',edged)
#cv2.waitKey(0)

contours, hierarchy = cv2.findContours(edged,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
cv2.imshow('canny edges after contouring', edged)
#cv2.waitKey(0)

print(contours)
print('Numbers of contours found=' + str(len(contours)))


# corner finder
'''
gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)
#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)
# Threshold for an optimal value, it may vary depending on the image.
image[dst>0.01*dst.max()]=[0,0,255]
cv2.imshow('dst',image)
#cv2.waitKey(0)
'''

'''
cv2.drawContours(image,contours,-1,(0,0,255),3)
cv2.imshow('contours',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''
