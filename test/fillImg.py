import cv2
import numpy as np
def draw_contours(img, cnts):  # conts = contours
    img = np.copy(img)
    img = cv2.drawContours(img, cnts, -1, (0, 255, 0), 2)
    return img


def draw_min_rect_circle(img, cnts):  # conts = contours
    img = np.copy(img)
    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        #cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), -1)
        min_rect = cv2.minAreaRect(cnt)  # min_area_rectangle
        min_rect = np.int0(cv2.boxPoints(min_rect))
        cv2.drawContours(img, [min_rect], 0, (255,255,255), -1)  # green
    return img

def draw_approx_hull_polygon(img, cnts):
    #img = np.copy(img)
    img = np.zeros(img.shape, dtype=np.uint8)

    cv2.drawContours(img, cnts, -1, (255, 0, 0), 2)  # blue

    epsilion = img.shape[0]/32
    approxes = [cv2.approxPolyDP(cnt, epsilion, True) for cnt in cnts]
    cv2.polylines(img, approxes, True, (0, 255, 0), 2)  # green

    hulls = [cv2.convexHull(cnt) for cnt in cnts]
    cv2.polylines(img, hulls, True, (0, 0, 255), 2)  # red
    return img


def runContours(image):
	edge=np.copy(image)
	thrs1 = cv2.getTrackbarPos('thrs1', 'edge')
	thrs2 = cv2.getTrackbarPos('thrs2', 'edge')
	#image=cv2.cvtColor(edge,cv2.COLOR_BGR2GRAY)
	thresh = cv2.Canny(edge, 1, 2, edge, 3, True)
	thresh, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_L1)
	for ct in contours:
		cv2.drawContours(image, ct, 0, (255,255,255) ,thickness=1)
	cv2.imshow("imgWithC  ontours",image)
	cv2.waitKey(0)
	

def openImg():
	img= cv2.imread('H:\Codes\IntelligentBuildingPerformanceDesign\\resources\detect45.jpg')
	return img

def runfilter(img):
	rows, cols = img.shape[:2]
	kernel_identity = np.array([[0,0,0], [0,1,0], [0,0,0]])
	kernel_3x3 = np.ones((3,3), np.float32) / 9.0 # Divide by 9 to normalize	the kernel
	kernel_5x5 = np.ones((5,5), np.float32) / 25.0 # Divide by 25 to normalize	the kernel
	cv2.imshow('Original', img)
	output = cv2.filter2D(img, -1, kernel_identity)
	cv2.imshow('Identity filter', output)
	output = cv2.filter2D(img, -1, kernel_3x3)
	cv2.imshow('3x3 filter', output)
	output = cv2.filter2D(img, -1, kernel_5x5)
	cv2.imshow('5x5 filter', output)
	cv2.waitKey(0)

def floodfillPlan(img):
	m,n,p=img.shape
	mask=np.zeros((m+2,n+2),np.uint8)
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	retval, image, mask, rect=cv2.floodFill(gray,mask,(0,0),(255,255,22),(100,43,46),(124,255,255),cv2.FLOODFILL_FIXED_RANGE)
	image2=np.copy(image)
	cv2.bitwise_not(image,image2)
	#cv2.imshow('FloodFill', image)
	cv2.imshow('FloodFillInverse', image2)
	cv2.waitKey(0)
	return image2

def blurImg(img):
	cv2.imshow('origin', img)
	gray=np.copy(img)
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gradX = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 1, dy = 0, ksize = -1)
	gradY = cv2.Sobel(gray, ddepth = cv2.CV_32F, dx = 0, dy = 1, ksize = -1)
	gradient = cv2.subtract(gradX, gradY)
	gradient = cv2.convertScaleAbs(gradient)
	blurred = cv2.blur(gradient, (2, 2))
	(_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
	#cv2.imshow('gray', blurred)
	img_dilation=dilation(blurred)
	#for i in range(10):
	cv2.waitKey(0)
	return img_dilation
	
def dilation(img):
	kernel = np.ones((2,2), np.uint8)
	img_dilation = cv2.dilate(img, kernel, iterations=1)
	cv2.imshow('Dilation', img_dilation)
	return img_dilation

def extractObjectByColor(img):
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
	lower_blue = np.array([80,150,150])
	upper_blue = np.array([124,255,255])

	mask = cv2.inRange(hsv,lower_blue,upper_blue)
	res = cv2.bitwise_and(img,img,mask=mask)
	cv2.imshow('frame', img)
	cv2.imshow('mask', mask)
	cv2.imshow('res', res)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	for y in range(res.shape[1]):
		for x in range(res.shape[0]):
			i = 0
			for z in range(3):
				if res.item(x,y,z) == 0 :
					i = i + 1
			if i == 3:
				res[x, y] = (255, 255, 255)
	cv2.imshow('res', res)
	cv2.waitKey(0)
def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            bin, contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares
def approxPolyDPtext(img,contours):
	FIRST = 0
	RED = (255,255,255)
	THICKNESS = 10
	imgcp=np.copy(img)
	largest=None
	for c in contours:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.01 * peri, True)
		if largest is None or cv2.contourArea(c) > cv2.contourArea(largest):
			largest=c
	cv2.drawContours(imgcp,[largest],FIRST, RED, THICKNESS)
	cv2.imshow("imgPolyDP",imgcp)
	
if __name__ == '__main__':
	img=openImg()
	#extractObjectByColor(img)
	#floodfillPlan(img)
    #blurredImg=blurImg(image)
    #extractObjectByColor(img)
	runContours(blurImg(img))

pass