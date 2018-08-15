import numpy as np
import cv2
im = cv2.imread('H:\Codes\IntelligentBuildingPerformanceDesign\\resources\\test.jpg')

imgray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY) #cv2.COLOR_BGR2GRAY

ret,thresh = cv2.threshold(imgray,127,255,0)
im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(im, contours, -1, (0,255,0), 3)
#cv2.drawContours(im, contours, 3, (0,255,0), 3)
#cnt = contours[4]
#cv2.drawContours(im, [cnt], 0, (0,255,0), 3)
