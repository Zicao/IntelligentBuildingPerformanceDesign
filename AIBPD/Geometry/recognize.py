'''
Purpose: recognize different objects in dxf files, such as external walls, pillars, 
Created: 04-05-2018
Copyright (C): TIAN ZHICHAO
'''
from sympy import Line, Point
import math
import ezdxf
import time
class __RecognizeBaseclass():
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

	def getParallelLines(self, line0,line1):
		# if they have same slope, they parallel to each other.
		xS0,yS0,zS0 =line0.dxf.start
		xE0,yE0,zE0 =line0.dxf.end
		xS1,yS1,zS1 =line1.dxf.start
		xE1,yE1,zE1 =line1.dxf.end
		if not xE0==xS0:
			slope0 = (yE0-yS0)/(xE0-xS0)
		else:
			slope0 = None
		if not xE1==xS1:
			slope1 = (yE1-yS1)/(xE1-xS1)
		else:
			slope0 = None
			
		if xE0==xS0 and xE1==xS1:
			distHorizon = xE0-xE1
			return distHorizon
		elif slope0 ==None or slope1==None:
			return False
		elif slope0 == slope1:
			alpha = math.atan(slope0)
			distVertical = slope0*(xE0-xE1)+yE1-yE0
			distHorizon = math.cos(alpha)*distVertical
			return distHorizon
		else:
			return False

	def isParallelLines(self, line0,line1):
		'''
		judge whether two lines are paralleled or not.
		Args:
			line0, a ezdxf Line object.
			line1, a ezdxf Line object
		'''
		results = getParallelLines(line0,line1)
		if not results:
			return True
		else:
			return False
	def isVerticalLines(self, line0,line1):
		'''
		judge whether two lines are vertical or not.if two lines are amost vertical to each other, we assume they are vertical to each other
		

		Args:
			line0, a ezdxf Line object.
			line1, a ezdxf Line object
		'''
		xS0,yS0,zS0 =line0.dxf.start
		xE0,yE0,zE0 =line0.dxf.end
		xS1,yS1,zS1 =line1.dxf.start
		xE1,yE1,zE1 =line1.dxf.end
		if (xS0==xE0 and yS1==yE1) or (xS1==xE1 and yS0==yE0):
			return True
		elif xE0!=xS0 and xE1!=xS1 and yE0!=yS0:
			slope0 = (yE0-yS0)/(xE0-xS0)
			slope1 = (yE1-yS1)/(xE1-xS1)
			if slope1-1/slope0<=0.01:
				return True
		else:
			return False


	def exWallConstraint(self, smallXLines, widthLimited = 600):
		'''

		'''
		n = len(smallXLines)
		i = 0
		parallel=[]
		while i < n:
			parallelList = []
			parallelList.append(smallXLines[i])
			for j in range(i,n):
				parallelTrue= self.getParallelLines(smallXLines[i],smallXLines[j])
				if parallelTrue and parallelTrue < widthLimited: #suppose that the width of the external wall small than 600
					parallelList.append(smallXLines[j])
			if len(parallelList)>1:
				parallel.append(parallelList)
			i+=1
			#sort lines that parallel to this line
		#for i in parallel:
			#print(i)
		return parallel  #store all lines into a list.
	def outerContourConstraint(self,startPoint, endPoint,xMax,xMin,yMax,yMin):
		'''

		Args:
			startPoint, dxf line object, i.e. (x,y,z)

		'''
		xSmall = xMin + 0.05* (xMax-xMin)
		ySmall = yMin + 0.1* (yMax-yMin)
		xBig = xMin + 0.95*(xMax-xMin)
		yBig = yMin + 0.95*(yMax-yMin)
		xS,yS,zS =startPoint
		xE,yE,zE =endPoint
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
	

	def isVerticalPolylines(self, pLine0, pLine1, pLine2):
		'''
		to judge whether two polylines (segment of polylines) are vertical or not
		Args:
			pLine0, LWPolyline object
			pLine1, LWPolyline object
			pLine2, LWPolyline object
		'''
		x0, y0,start_width0, end_width0,bulge0 = pLine0
		x1, y1,start_width1, end_width1,bulge1 = pLine1
		x2, y2,start_width2, end_width2,bulge2 = pLine2

		if (x0==x1 and y1==y2) or (y0==y1 and x1==x2):
			return True
		elif x0!=x1 and x1!=x2 and y2!=y1:
			slope0=(y1-y0)/(x1-x0)
			slope1=(y2-y1)/(x2-x1)
			if slope0-1/slope1<=0.01:
				return True
		else:
			return False

	def convertLWPolylinesIntoLines(self,msp,msp1):
		lines=[]
		LWPolylines = msp.query('LWPOLYLINE')
		for LWPLine in LWPolylines:
			with LWPLine.points() as points:
				n = len(points)
				for i in range(n-1):
					xS, yS, start_widthS, end_widthS, bulgeS = points[0]
					xE, yE, start_widthE, end_widthE, bulgeE = points[1]
					msp1.add_line((xS, yS,0),(xE, yE,0))

	def convertLWPolylinesIntoLines(self,msp,lines):
		'''

		'''
		print("Beginning of transform all LWPolyline and Polylines into Lines objects")
		tBegin=time.time()
		line0=Line((0,0),(0,1))
		LWPolylines = msp.query('LWPOLYLINE')
		for LWPLine in LWPolylines:
			with LWPLine.points() as points:
				n = len(points)
				for i in range(n-1):
					xS, yS, start_widthS, end_widthS, bulgeS = points[0]
					xE, yE, start_widthE, end_widthE, bulgeE = points[1]
					line0=Line((xS, yS),(xE, yE))
					lines.append(line0)
		polylines=msp.query('POLYLINE')
		for pLine in polylines:
			with pLine.points() as points:
				n = len(points)
				for i in range(n-1):
					xS, yS, start_widthS, end_widthS, bulgeS = points[0]
					xE, yE, start_widthE, end_widthE, bulgeE = points[1]
					line0=Line((xS, yS),(xE, yE))
					lines.append(line0)
		print("End of transforming. Time cost", time.time()-tBegin)
		return lines
	def convertPolylinesIntoLines(self, msp,lines):

		pass
	

class Recognize(__RecognizeBaseclass):
	'''

	'''
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
					smallXLines.append(e)
				elif xS>xBig and xE> xBig:
					bigXLines.append(e)
				elif yS< ySmall and yE < ySmall:
					smallYLines.append(e)
				elif yS > yBig and yE >yBig:
					bigYLines.append(e)
		xSmallExWall = 	self.exWallConstraint(smallXLines,widthLimited = 600)
		xBigExWall = self.exWallConstraint(bigXLines, widthLimited = 600)
		ySmallExWall = self.exWallConstraint(smallYLines,widthLimited = 600)
		yBigExWall = self.exWallConstraint(bigYLines, widthLimited = 600)
		return xSmallExWall, xBigExWall, ySmallExWall, yBigExWall

	def recognizeLWPolylinePillar(self, pLines,xMax,xMin,yMax,yMin):
		'''
		regognize pillars in the dxf files.
		Args:
			pLines, PWPolyline object
		'''
		i=0
		
		pillarsPlines = []

		for line in pLines:
			with line.points() as linePoints:
				n = len(linePoints)
				if n<=3:
					next
				for i in range(n-2):
					if self.isVerticalPolylines(linePoints[i],linePoints[i+1],linePoints[i+2]):
						x0, y0,start_width0, end_width0,bulge0 = linePoints[i]
						x1, y1,start_width1, end_width1,bulge1 = linePoints[i+1]
						x2, y2,start_width2, end_width2,bulge2 = linePoints[i+2]
						isTrue0=self.outerContourConstraint((x0, y0,0), (x1, y1,0),xMax,xMin,yMax,yMin)
						isTrue1=self.outerContourConstraint((x1, y1,0), (x2, y2,0),xMax,xMin,yMax,yMin)
						i+=1
						if i>=3 and isTrue0 and isTrue1:
							pillarsPlines.append(line)
					else:
						i=0

		return pillarsPlines

	def recognizeStairs(self,msp):
		'''
		recognize the Stairs in the msp files. Once recognize one stair save it into a new
		file and record the main ordinates.
		
		'''
		pass

	def reconizeExteriorWindowFromLWPolylines(self, msp):
		'''
		recognize all the exterior windows, same object into list.

		Args:
			msp, the modelspace of the dxf file.

		'''
		exWindowLists = []
		
		return exWindowLists
	def dividedLinesIntoSmallGroup(self, lines, msp):
		for e in msp:
			if e.dxftype() == 'LINE':
				lines.append(e)
		smallGroup=[]
		n=len(lines)
		groupNum=int(n/30)+1
		for i in range(groupNum):
			smallGroup.append([])
		for line in lines:
			xS0,yS0,zS0= line.dxf.start
			xE0,yE0,zE0= line.dxf.end
			pS0,pE0 = Point(xS0,yS0), Point(xE0,yE0)
			syLine0Length = pS0.distance(pE0)
			if not (syLine0Length>=3000 or syLine0Length<500):
				i=int(groupNum*(syLine0Length-500)/(3000-500))
				smallGroup[i].append(line)
		#smallGroup=self.divideSmallGroupIntoPiece(smallGroup)
		for x in smallGroup:
			print(len(x))
		return smallGroup

	def getMaxMinLength(self, lineList):
		maxvalue, minvalue = 0,0
		i=1
		for line in lineList:
			#syLine0 = Line((xS0,yS0),(xE0,yE0))
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

	def reconizeExteriorWindowFromLines(self, msp):
		'''
		recognize all the exterior windows, same object into list.

		Args:
			msp, the modelspace of the dxf file.

		'''
		exWindowLists = []
		
		lines = []
		segmentLines=[]
		for e in msp:
			if e.dxftype() == 'LINE':
				lines.append(e)
		print("number of lines",len(lines))
		N=15
		t0=time.time()
		groupNum = int(len(lines)/N)+1
		for i in range(groupNum-1):
			segmentLines.append(lines[N*i:N*(i+1)])
		segmentLines.append(lines[(groupNum-1)*N:])
		'''for i in range(16):
			segmentLines.append([])
		t0=time.time()
		for line in lines:
			xS0,yS0,zS0= line.dxf.start
			xE0,yE0,zE0= line.dxf.end
			#syLine0 = Line((xS0,yS0),(xE0,yE0))
			pS0,pE0 = Point(xS0,yS0), Point(xE0,yE0)
			syLine0Length = pS0.distance(pE0) # length of this line
			if syLine0Length<=600 and syLine0Length>=550:
				segmentLines[0].append(line)
			elif syLine0Length<=700:
				segmentLines[1].append(line)
			elif syLine0Length<=800:
				segmentLines[2].append(line)
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
			elif syLine0Length<=2300:
				segmentLines[15].append(line)
			elif syLine0Length<=2400:
				segmentLines[12].append(line)
			elif syLine0Length<=2700:
				segmentLines[13].append(line)
			elif syLine0Length<=3000:
				segmentLines[14].append(line)
		print(time.time()-t0)
		for i in range(16):
			print("segmentList",i,len(segmentLines[i]))
		print("beginning of divided")
		'''
		
		#self.divideSmallGroupIntoPiece(segmentLines)
		#print("end of divided",time.time()-t0)

		for segmentLine in segmentLines:
			print(len(segmentLine))
		for linesGroup in segmentLines:
			t0=time.time()
			while len(linesGroup):
				line0 = linesGroup[0]
				xS0,yS0,zS0= line0.dxf.start #A point
				xE0,yE0,zE0= line0.dxf.end #B point
				syLine0 = Line((xS0,yS0),(xE0,yE0))
				pS0,pE0 = Point(xS0,yS0), Point(xE0,yE0)
				#syLine0Length = pS0.distance(pE0) # length of this line
				exWindowLine = []
				exWindowLine.append(line0)
				i=1
				while i<len(linesGroup):
					line1=linesGroup[i]
					xS1,yS1,zS1= line1.dxf.start #C point
					xE1,yE1,zE1= line1.dxf.end #D point
					syLine1 = Line((xS1,yS1),(xE1,yE1))
					pS1,pE1 = Point(xS1,yS1), Point(xE1,yE1)
					#syLine1Length = pS1.distance(pE1) # distance of point C and point D
					distanceAC = pS0.distance(pS1) # distance of point A and point C
					distanceBD = pE0.distance(pE1) 
					distanceAD = pS0.distance(pE1)
					distanceBC = pE0.distance(pS1)
					distanceTosyLine0 = syLine1.distance(pS0) # the distance between point A and line1
					if pS0==pS1 or pS0==pE1 or pS0==pE0:
						i+=1
					elif Line.is_parallel(syLine0,syLine1) and distanceAC==distanceBD and distanceAD==distanceBC and distanceTosyLine0<=300:
						#three criteria used to judge whether these two lines belong to same window
						#These two lines are parallel to each other.
						#These two lines have same length.
						#The distance between these two lines smaller than 0.3m
						exWindowLine.append(line1)
						del linesGroup[i]
					else:
						i+=1
				del linesGroup[0]
				if len(exWindowLine)>1:
					exWindowLists.append(exWindowLine)
			print(time.time()-t0)
		return exWindowLists

	def recognizeExteriorWindowFromPoints(self, lines):
		'''
		this function recognize windows from  lines that are sympy Line objects transformed
		from LWPolylines and polylines.

		Args:
			lines, sympy Line objects which are generated from LWPloylines and polylines.
		'''
		exWindowLists=[]
		otherLineLists=[]
		otherLineLists1=[]
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
			t0=time.time()
			while len(linesGroup):
				line0 = linesGroup[0]
				pS0,pE0 = line0.p1, line0.p2
				syLine0Length = line0.p1.distance(line0.p2)
				#syLine0Length = pS0.distance(pE0) # length of this line
				exWindowLine = []
				exWindowLine.append(line0)
				i=1
				while i<len(linesGroup):
					line1=linesGroup[i]
					pS1,pE1 = line1.p1, line1.p2
					#syLine1Length = pS1.distance(pE1) # distance of point C and point D
					distanceAC = pS0.distance(pS1) # distance of point A and point C
					distanceBD = pE0.distance(pE1) 
					distanceAD = pS0.distance(pE1)
					distanceBC = pE0.distance(pS1)
					distanceTosyLine0 = line1.distance(pS0) # the distance between point A and line1
					'''print("line0",line0,"line1",line1,"parallel?",Line.is_parallel(line0,line1))
					print("length of AC",distanceAC,"distance of BC",distanceBC,"length of AD",distanceAD,"length of BD",distanceBD)
					print("AC==BD?",distanceAC-distanceBD<0.01)
					print("AD==BC?",distanceAD-distanceBC<0.01)'''
					if pS0==pS1 or pS0==pE1 or pS0==pE0:
						i+=1
						otherLineLists.append(line1)
					elif distanceAC-distanceBD<=0.01 and distanceAD-distanceBC<=0.01 and distanceTosyLine0<=300:
						#three criteria used to judge whether these two lines belong to same window
						#These two lines are parallel to each other.
						#These two lines have same length.
						#The distance between these two lines smaller than 0.3m
						exWindowLine.append(line1)
						del linesGroup[i]
					else:
						otherLineLists1.append(line1)
						i+=1
				del linesGroup[0]
				if len(exWindowLine)>1:#issues occured here. Since no lines are pap
					exWindowLists.append(exWindowLine)
			print("for group",len(linesGroup),time.time()-t0)
		return exWindowLists,otherLineLists,otherLineLists1