'''
Purpose: recognize different objects in dxf files, such as external walls, pillars, 
Created: 04-05-2018
Copyright (C): TIAN ZHICHAO
'''
import sympy
import math
import ezdxf
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