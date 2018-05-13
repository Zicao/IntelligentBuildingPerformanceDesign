'''

'''

import numpy as np
import math
import recognize
import ezdxf
from sympy import Point, Line
import time

def print_entity(e):
    print("LINE on layer: %s\n" % e.dxf.layer)
    print(e.dxf.start)

def extendExWall(P0,P1,l1,msp):
	l0=Line(p0,p1)
	intersectedPoint = l0.intersection(l1)
	xE,yE = intersectedPoint
	xS,yS = p1
	msp.add_line(((xS, yS,0),(xE, yE,0)))
	l0=Line(p1,intersectedPoint)
	return l0



def drawExWall(xSmallExWall, xBigExWall, ySmallExWall, yBigExWall, msp):
	'''
	Draw external wall lines. 
	uppose that buildings are ractangle.
	Args:
		xSmallExWall,
		xBigExWall,
		ySmallExWall,
		yBigExWall,
		msp, en ezdxf.modelspace() object used to create a new dxf file.
	'''
	recognizeObject=recognize.Recognize()
	xMax,xMin,yMax,yMin = recognizeObject.getExtremePointInLines(xSmallExWall)
	msp.add_line((xMin,yMin,0),(xMin,yMax,0))  # add a LINE entity

	'''xMax,xMin,yMax,yMin = recognizeObject.getExtremePointInLines(xBigExWall)
	msp.add_line((xMax,yMin,0),(xMax,yMax,0))  # add a LINE entity
	xMax,xMin,yMax,yMin = recognizeObject.getExtremePointInLines(ySmallExWall)
	msp.add_line((xMin,yMin,0),(xMax,yMin,0))  # add a LINE entity
	xMax,xMin,yMax,yMin = recognizeObject.getExtremePointInLines(yBigExWall)
	msp.add_line((xMin,yMax,0),(xMax,yMax,0))  # add a LINE entity
	'''
	del recognizeObject
	return Point(xMin,yMin), Point(xMin,yMax)

def drawPillars(plinePillarList, msp):
	xS, yS,start_widthS, end_widthS, bulgeS = (0.0,0.0,0.0,0.0,0.0)
	for line in plinePillarList:
		i=0
		with line.points() as points:
			n= len(points)
			for point in points:
				if i==0:
					x0, y0,start_width0, end_width0, bulge0 = point
					xS, yS,start_widthS, end_widthS, bulgeS = point
				elif i<(n):
					x1, y1,start_width1, end_width1,bulge1 = point
					msp.add_line((x0, y0,0),(x1, y1,0))
					x0, y0,start_width0, end_width0, bulge0 = x1, y1,start_width1, end_width1,bulge1
				else:
					msp.add_line((x1, y1,0),(xS, yS,0))
				i+=1
def drawOuterContour(initPoint,existMsp,newMsp):
	'''
	draw the buildong outer contour by seaching and recognize objects in existMsp.
	Args:
		initPoint, the start point.
		existMsp, exist dxf file.
		newMsp, the modelspace of the new dxf file.
	'''
	pass
	

if __name__=="__main__":
	dwg = ezdxf.readfile("../../resources/QiangongF12010.dxf")
	msp = dwg.modelspace()
	recognizeObjects=recognize.Recognize()
	dwg2 = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'
	msp2 = dwg2.modelspace()
	dwg3 = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'
	msp3 = dwg3.modelspace()
	dwg4 = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'
	msp4 = dwg4.modelspace()
	lines=[]
	lines=recognizeObjects.convertLWPolylinesIntoLines(msp,lines)
	ExWindowLines, otherLines,otherLines1=recognizeObjects.recognizeExteriorWindowFromPoints(lines)
	for windowLines in ExWindowLines:
		for line in windowLines:
			msp2.add_line(line.p1,line.p2)
	dwg2.saveas('../../resources/line8.dxf')
	for line in otherLines:
		msp3.add_line(line.p1,line.p2)
	dwg3.saveas('../../resources/line9.dxf')
	for line in otherLines1:
		msp4.add_line(line.p1,line.p2)
	dwg4.saveas('../../resources/line10.dxf')


	'''
	xSmallExWall, xBigExWall, ySmallExWall, yBigExWall = recognizeObjects.sortExternalWall(xMax,xMin,yMax,yMin,msp)
	p0,p1 = drawExWall(xSmallExWall, xBigExWall, ySmallExWall, yBigExWall, msp3)
	line = msp.query('LWPOLYLINE')
	pillarPlinesList = recognizeObjects.recognizeLWPolylinePillar(line,xMax,xMin,yMax,yMin)
	drawPillars(pillarPlinesList, msp3)
'''