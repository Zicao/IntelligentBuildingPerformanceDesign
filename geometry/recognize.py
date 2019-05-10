'''
Purpose: recognize different objects in dxf files, such as external walls, pillars, 
Created: 04-05-2018
Copyright (C): TIAN ZHICHAO, tzchao123@qq.com.
'''
#from sympy import Line, Point
import math
import ezdxf
import time
import sys
import os
import re

from aibpd.utility.line import Line
class __RecognizeBaseclass():
	'''
	add functions to get the basic attributes of the dxf file, such as Area, Contour
	'''
	xMax,xMin,yMax,yMin=0.0, 0.0, 0.0, 0.0
	#coordinates of the extreme points in the dxf file
	

	"""docstring for __RecognizeBaseclass"""
	def __init__(self):
		pass
	def getMaxMin(self,x1,x2,xMax,xMin):
		if x1>xMax:
			xMax = x1
		if x2>xMax:
			xMax = x2
		if x1<xMin:
			xMin = x1
		if x2<xMin:
			xMin = x2
		return xMax,xMin

	def getExtremePointInLines(self, Lines):
		'''
		get the coordinates of extreme points in the dxf map.
		These points will be used to create the contour the building.
		Args:
			Lines, Line object list typically contains all the lins object in the dxf file

		'''
		xMax = 0.0
		yMax = 0.0
		xMin = 0.0
		yMin = 0.0
		i=1
		for X in Lines:
			for e in X:
				xStart,yStart,z0= e.dxf.start
				xEnd,yEnd,z1= e.dxf.end
				x2Avrg= (xStart+xEnd)/2
				y2Avrg= (yStart+yEnd)/2
				if i ==1:
					xMin=x2Avrg
					yMin=y2Avrg
				xMax,xMin = self.getMaxMin(xStart,xEnd,xMax,xMin)
				yMax,yMin = self.getMaxMin(yStart,yEnd,yMax,yMin)
				i+=1
		return xMax,xMin,yMax,yMin


	def getLinesAtributes(self, msp):
		i=0
		xSum = 0.0
		ySum = 0.0
		xMax = 0.0
		yMax = 0.0
		xMin = 0.0
		yMin = 0.0
		
		for e in msp:
			if e.dxftype() == 'LINE':
				xStart,yStart,z0= e.dxf.start
				xEnd,yEnd,z1= e.dxf.end
				x2Avrg= (xStart+xEnd)/2
				y2Avrg= (yStart+yEnd)/2
				xSum +=x2Avrg
				ySum +=y2Avrg
				if i ==1:
					xMin=x2Avrg
					yMin=y2Avrg
				
				xMax,xMin = self.getMaxMin(xStart,xEnd,xMax,xMin)
				yMax,yMin = self.getMaxMin(yStart,yEnd,yMax,yMin)
				i+=1
		try:
			xAvrg = xSum/i
			yAvrg = ySum/i
		except Exception:
			print("there is no line in def file")
		return xMax,xMin,yMax,yMin,xAvrg,yAvrg

	def exWallConstraint(self, smallXLines, widthLimited = 600):
		'''
		sort out exterior walls
		Args:
			smallXLines, lines with small X axis value.
		'''
		n = len(smallXLines)
		i = 0
		parallel=[]
		while i < n:
			parallelList = []
			parallelList.append(smallXLines[i])
			for j in range(i,n):
				parallelTrue= smallXLines[i].isParallel(smallXLines[j])
				if parallelTrue and parallelTrue < widthLimited: #suppose that the width of the external wall small than 600
					parallelList.append(smallXLines[j])
			if len(parallelList)>1:
				parallel.append(parallelList)
			i+=1
		return parallel  #store all lines into a list.

	def outerContourConstraint(self,startPoint, endPoint,xMax,xMin,yMax,yMin):
		'''
		sort out objects that near the contour (exterior walls).
		For example, sort out pillars near the exterior walls.
		Args:
			startPoint, Point object.
			endPoint, Point object.
			
		'''
		xSmall = xMin + 0.05* (xMax-xMin)
		ySmall = yMin + 0.1* (yMax-yMin)
		xBig = xMin + 0.95*(xMax-xMin)
		yBig = yMin + 0.95*(yMax-yMin)
		xS,yS =startPoint.X, startPoint.Y
		xE,yE =endPoint.X, endPoint.Y
		if xS < xSmall and xE < xSmall:
			return True
		elif xS>xBig and xE> xBig:
			return True
		elif yS< ySmall and yE < ySmall:
			return True
		elif yS > yBig and yE >yBig:
			return True
		else:
			return False
	

	


class Recognize(__RecognizeBaseclass):
	

	def __init__(self):
		pass

	def sortExternalWall(self, xMax,xMin,yMax,yMin,msp):
		'''
		
		'''
		# sort out line with small x axis
		smallXLines = []
		bigXLines = []
		smallYLines = []
		bigYLines = []
		xSmall = xMin + 0.05* (xMax-xMin)
		ySmall = yMin + 0.1* (yMax-yMin)
		xBig = xMin + 0.95*(xMax-xMin)
		yBig = yMin + 0.95*(yMax-yMin)
		
		for e in msp:
			if e.dxftype() == 'LINE':
				xS,yS,zS =e.dxf.start
				xE,yE,zE =e.dxf.end
				if xS < xSmall and xE < xSmall:
					smallXLines.append(Line((xS,yS),(xE,yE)))
				elif xS>xBig and xE> xBig:
					bigXLines.append(Line((xS,yS),(xE,yE)))
				elif yS< ySmall and yE < ySmall:
					smallYLines.append(Line((xS,yS),(xE,yE)))
				elif yS > yBig and yE >yBig:
					bigYLines.append(Line((xS,yS),(xE,yE)))

		xSmallExWall = 	self.exWallConstraint(smallXLines,widthLimited = 600)
		xBigExWall = self.exWallConstraint(bigXLines, widthLimited = 600)
		ySmallExWall = self.exWallConstraint(smallYLines,widthLimited = 600)
		yBigExWall = self.exWallConstraint(bigYLines, widthLimited = 600)
		return xSmallExWall, xBigExWall, ySmallExWall, yBigExWall

	def getMaxMinLength(self, lineList):
		'''
		get the max and min length of lines in lineList
		Args:
			lineList: a list of Line objects
		'''
		maxvalue, minvalue = 0,0
		i=1
		for line in lineList:
			pS0,pE0 = line.p1,line.p2
			syLine0Length = pS0.distance(pE0)
			if i==1:
				maxvalue, minvalue=syLine0Length,syLine0Length
			else:
				if syLine0Length>=maxvalue:
					maxvalue=syLine0Length
				elif syLine0Length<=minvalue:
					minvalue=syLine0Length
			i+=1
		return maxvalue,minvalue

	def divideSmallGroupIntoPiece(self, bigGroup):
		'''
		divided bigGroup into two small group
		'''
		leftSmallGroup=[]
		rightSmallGroup=[]
		#syLine0LengthR=0.0
		i=0
		totalNumElement=0
		for groupElement in bigGroup:
			maxLength,minLength=self.getMaxMinLength(groupElement)
			totalNumElement+=len(groupElement)
			#print("num of elements",len(groupElement),"totalNum",totalNumElement)

			if len(groupElement)>30 and maxLength!=minLength:
				print("divided is working")
				syLine0LengthR = (maxLength+minLength)/2
				for line in groupElement:
					pS0,pE0=line.p1,line.p2
					syLine0Length = pS0.distance(pE0)
					if syLine0Length>=syLine0LengthR:
						leftSmallGroup.append(line)
					else:
						rightSmallGroup.append(line)
				if len(leftSmallGroup)>0 and len(rightSmallGroup)>0:
					bigGroup[i]=leftSmallGroup
					bigGroup.insert(i,rightSmallGroup)
					print("divided",len(groupElement),"into",len(leftSmallGroup),len(rightSmallGroup))
					self.divideSmallGroupIntoPiece(bigGroup)
			elif len(groupElement)>30 and maxLength==minLength:
				bigGroup[i]=groupElement[0:30]
				bigGroup.insert(i,groupElement[30:])
			i+=1
	def byLayerName(self, msp):
		'''
		delete columns, stairs, text etc.
		'''
		for i in msp:
			if re.search(i.dxf.layer.name,'column轴stair楼梯axis轴线EquipmentTEXT'):

class RecognizeExWall():
	'''
	Recognize the outlines of a building plan.
	'''
	def __init__():
		pass

	def recognizeExteriorWindowFromPoints(self, lines):
		'''
		this function recognize windows from  lines that are sympy Line objects transformed
		from LWPolylines and polylines.

		Args:
			lines, Line objects which are generated from LWPloylines and polylines.
		'''
		exWindowLists=[]
		segmentLines=[]
		
		N=15
		groupNum = int(len(lines)/N)+1
		for i in range(groupNum-1):
			segmentLines.append(lines[N*i:N*(i+1)])
		segmentLines.append(lines[(groupNum-1)*N:])
		
		'''
		t0=time.time()
		for i in range(15):
			segmentLines.append([])
		for line in lines:
			pS0,pE0 = line.p1,line.p2
			syLine0Length = pS0.distance(pE0) # length of this line
			if syLine0Length<=600 and syLine0Length>=550:
				segmentLines[0].append(line)
			elif syLine0Length<=700:
				#segmentLines[1].append(line)
			elif syLine0Length<=800:
				#segmentLines[2].append(line)
			elif syLine0Length<=900:
				segmentLines[3].append(line)
			elif syLine0Length<=1000:
				segmentLines[4].append(line)
			elif syLine0Length<=1200:
				segmentLines[5].append(line)
			elif syLine0Length<=1500:
				segmentLines[6].append(line)
			elif syLine0Length<=1600:
				segmentLines[7].append(line)
			elif syLine0Length<=1700:
				segmentLines[8].append(line)
			elif syLine0Length<=1800:
				segmentLines[9].append(line)
			elif syLine0Length<=2100:
				segmentLines[10].append(line)
			elif syLine0Length<=2250:
				segmentLines[11].append(line)
			elif syLine0Length<=2400:
				segmentLines[12].append(line)
			elif syLine0Length<=2700:
				segmentLines[13].append(line)
			elif syLine0Length<=3000:
				segmentLines[14].append(line)
		for i in range(15):
			print("segmentList",i,len(segmentLines[i]))
		self.divideSmallGroupIntoPiece(segmentLines)
		print("end of divided",time.time()-t0)'''
		for linesGroup in segmentLines:
			while len(linesGroup):
				line0 = linesGroup[0]
				pS0,pE0 = line0.p1, line0.p2 #A,B
				syLine0Length = line0.p1.distance(line0.p2)
				#syLine0Length = pS0.distance(pE0) # length of this line
				exWindowLine = []
				exWindowLine.append(line0)
				#print("old exWindowLine length",len(exWindowLine))
				i=1
				while i<len(linesGroup):
					line1=linesGroup[i]
					pS1,pE1 = line1.p1, line1.p2 #CD
					distanceAC = pS0.distance(pS1) # distance of point A and point C
					distanceBD = pE0.distance(pE1) 
					distanceAD = pS0.distance(pE1)
					distanceBC = pE0.distance(pS1)
					deltaDistanceAC_BD=math.fabs(distanceAC-distanceBD)
					deltaDistanceAD_BD =math.fabs(distanceAD-distanceBC)
					deltaDistanceAB_CD=math.fabs(line0.length()-line1.length())
					distanceTosyLine0 = math.fabs(line1.distance(pS0)) # the distance between point A and line1
					if (pS0.X==pS1.X and pS0.Y==pS1.Y) or (line0.p2.X==line1.p2.X and line0.p2.Y==line1.p2.Y):
						i+=1
					elif distanceAC>=10  and distanceAC<=300 and deltaDistanceAC_BD<=1 and deltaDistanceAD_BD<=1 and deltaDistanceAB_CD<=1:
						#three criteria used to judge whether these two lines belong to same window
						#These two lines are parallel to each other.
						#These two lines have same length.
						#The distance between these two lines smaller than 0.3m
						exWindowLine.append(line1)
						del linesGroup[i]
					else:
						i+=1
				del linesGroup[0]
				if len(exWindowLine)>=2:#issues occured here. Since no lines are pap
					#print("len(exWindowLine)",len(exWindowLine))
					exWindowLists.append(exWindowLine)
		return exWindowLists

	def exWallFromAxis(self, mspLines):
		'''
		regonize exterior outlines of the building plan from the axis.
		Args:
			mspLines, model space lines
		'''
		axisLines=[]
		#get lines whose layers names contain "axis"
		for line in mspLines:
			if re.search('axis',line.layer.name,re.I) or \
				re.search('轴线'.encode('uft8'),line.layer.name.encode('utf8')):
				axisLines.append(line)
		outmostAxisLines=[]
		#filtrate outmost axis
		for line in axisLines:
			
		del axisLines
class RecognizeAxis(Recognize):
	'''
	recognize all the axis in the dxf file.
	'''
	def __init__(self):
		pass
	def byLayerName(self):
		'''
		recognize axis by their name. Their layer name may contain "axis, or 轴线 etc"
		Args:	
		
		'''
		pass
	def byLength(self):
		'''
		Axis belong to the longest axis.
		'''
		pass
class RecognizeDoor(Recognize):
	'''
	recognize all the doors in the dxf file.
	'''
	def __init__(self):
		pass

	def byShape(self):
		'''
		Recognize doors by their shape. For example, a door may looks like a quadrant.
		'''
		pass
class RecognizePillar(Recognize):
	'''
	Recognize all the pillars in the dxf file
	'''
	def __init__(self):
		pass

	def byShape(self):
		pass

	def recognizePillar(self, lineList,xMax,xMin,yMax,yMin):
		'''
		regognize pillars in the dxf files.
		Args:
			lineList, a 2D list of Line objects which are transformed from ezdxf LWPolyline.
		each lineList object contains lines transformed from a LWPolyline or Polyline
		'''
		i=0
		
		pillarsLines = [] # a 2D list of object used to store lines that form a pillar

		for linesPerPolyline in lineList:
			n=len(linesPerPolyline)
			if n<=3:
				next
			else:
				#judge whether these lines in linesPerPolyline are vertical to each other
				i=0
				j=[]
				while i<n-1:
					if linesPerPolyline[i].isVertical(linesPerPolyline[i+1]):
						#the lines in sequence of rectangle pillars are vertical to each other
						isTrue0=self.outerContourConstraint(linesPerPolyline[i].x,linesPerPolyline[i].y,xMax,xMin,yMax,yMin)
						#judge whether the pillar are near the external wall or not.
						isTrue1=self.outerContourConstraint(linesPerPolyline[i+1].x,linesPerPolyline[i+1].y,xMax,xMin,yMax,yMin)
						#judge whether the pillar are near the outer contour constraint or not.
						if isTrue0 and isTrue1:
							j.append(1)
					else:
						j.append(0)
					i+=1
				if not 0 in j:
					pillarsLines.append(linesPerPolyline)
		return pillarsLines

class RecognizeExWin(Recognize):
	'''

	'''
	def __init__(self):
		pass
	def fromLWPolylines(self, msp):
		'''
		recognize all the exterior windows, same object into list.

		Args:
			msp, the modelspace of the dxf file.

		'''
		exWindowLists = []
		
		return exWindowLists
class RecognizeStair(Recognize):
	'''
	Recognize all the stairs in the dxf file.
	'''
	def __init__(self):
		pass

	def byShape(self,msp):
		'''
		recognize the Stairs in the msp files. Once recognize one stair save it into a new
		file and record the main ordinates.
		
		'''
		pass

	def byLayerName(self,msp):
		'''
		
		'''



class RecognizeAtrium(self):
	'''
	Recognize all the atrium
	'''
	def __init__(self):
		pass

	def recognizeAtrium(self,msp):
		'''
		recognize atriums in the dxf file.
		Args:
			msp, the ezdxf modelplace objects which contains all the data
		'''