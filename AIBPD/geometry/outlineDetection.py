import numpy as np
import cv2

from IntelligentBuildingPerformanceDesign.utility.line import Line
def drawHoughLines():
	
	rgb = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
	#imgray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	gray = cv2.cvtColor(cv2.cvtColor(im,cv2.COLOR_HSV2BGR), cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,50,150,apertureSize = 3)
	lines = cv2.HoughLinesP(edges,20,np.pi/90,110)
	line_count = lines.shape[0]
	print(lines)
	angle = 0
	count = 0

	for x in range(line_count):

		for rho,theta in lines[x]:
			a = np.cos(theta)
			b = np.sin(theta)
	        #print(theta)
			x0 = a*rho
			y0 = b*rho
			x1 = int(x0 + 1000*(-b))
			y1 = int(y0 + 1000*(a))
			x2 = int(x0 - 1000*(-b))
			y2 = int(y0 - 1000*(a))

			crr_angle = np.degrees(b)
			if (crr_angle < 5):
	            #print(crr_angle)
				angle = angle + crr_angle
				count = count + 1
				cv2.line(rgb,(x1,y1),(x2,y2),(0,0,255),2)
	angle = angle / count
	print(angle)
	cv2.imshow('rgb',rgb)
	cv2.waitKey(0)
	
def drawHoughLinesP(img):
	edges = cv2.Canny(img,250,500)
	threshold = 60
	minLineLength = 5
	lines = cv2.HoughLinesP(edges, 0.2, np.pi/90, threshold, 0, minLineLength, 20);
	if (lines is None or len(lines) == 0):
	  return
	groups=[]
	
	linesList=lines.tolist()
	deleteOverlapLine(linesList,groups)
	img2=np.copy(img)
	img3=np.copy(img)
	for group in groups:
		lines=[]
		for opencvlines in group: #
			for opencvline in opencvlines: #[0,0,1,1]
				line=Line((opencvline[0],opencvline[1]),(opencvline[2],opencvline[3]))
				lines.append(line)
		extendedLine=extendOverlapLines(lines)
		x1=int(extendedLine.p1.x)
		y1=int(extendedLine.p1.y)
		x2=int(extendedLine.p2.x)
		y2=int(extendedLine.p2.y)
		cv2.line(img,(x1,y1),(x2,y2), (0,255,0), 2)
	cv2.imshow("line_img2", img2)
	cv2.imshow("lines.jpg", img)
	cv2.waitKey(0)
	
def deleteOverlapLine(lines,groups):
	'''
	Delete overlaped parallel lines.
	Args:
		Lines, which is a 3-dimensional list.
		groups, a empty list used to contain lines parallel to each other.
	'''
	remainingLines=[]
	paralleledLines=[]
	paralleledLines.append(lines[0])
	line1=Line((lines[0][0][0],lines[0][0][1]), (lines[0][0][2],lines[0][0][3]))
	m=len(lines)
	#print('length of lines',m)
	for i in range(2,m):
		line2=Line((lines[i][0][0],lines[i][0][1]), (lines[i][0][2],lines[i][0][3]))
		#print('distanceBetweenLines',line1.distance(line2.p1))
		#print('anglesBetweenLines',line1.theta-line2.theta)
		if line1.distanceOfParallelLines(line2,20):
			paralleledLines.append(lines[i])
		else:
			remainingLines.append(lines[i])
	groups.append(paralleledLines)
	#print('length of paralleledLines',len(paralleledLines))
	#print('length of groups',len(groups))
	#print('length of remainingLines',len(remainingLines))
	if m==1:
		return
	else:
		if remainingLines:
			deleteOverlapLine(remainingLines,groups)
		else:
			return
def extendOverlapLines(lines):
	'''
	extend overlap lines (mutually paralleled with small distance) into a long line.
	Args:
		lines: list object contain several parallel lines object.
	Examples:

	'''
	maxLength=0.0
	maxLine=Line((0,0),(0,0.1))
	for line in lines:
		if line.length>maxLength:
			maxLength=line.length
			maxLine=line
	#get the distance between points and central point of maxLine
	#if the distance longer than half of maxlength, extend this line.
	interactedPoint=None
	for line1 in lines:
		'''x1=int(line1.p1.x)
		y1=int(line1.p1.y)
		x2=int(line1.p2.x)
		y2=int(line1.p2.y)
		cv2.line(img,(x1,y1),(x2,y2), (0,0,255), 2)
		for p in [line1.p1,line1.p2]:
			if p.distance(maxLine.midpoint)>maxLength/2:
				interactedPoint=maxLine.interactedPointofTwoLines(line1)

		if interactedPoint:
			if maxLine.p1.distance(interactedPoint)>maxLine.p2.distance(interactedPoint)\
				and maxLine.p1.distance(interactedPoint)>maxLine.length:
				maxLine.p2=interactedPoint
			elif maxLine.p2.distance(interactedPoint)>maxLine.p1.distance(interactedPoint)\
				and maxLine.p2.distance(interactedPoint)>maxLine.length:
				maxLine.p1=interactedPoint'''
	
	return Line(endPoint1=maxLine.p1,endPoint2=maxLine.p2)
	
	
if __name__=="__main__":
	im = cv2.imread('C:\\Users\\tzcha\\Documents\\IntelligentBuildingPerformanceDesign\\resources\\detect4.jpg')
	if im is not None:
		drawHoughLinesP(im)
	else:
		print('please check your files')


