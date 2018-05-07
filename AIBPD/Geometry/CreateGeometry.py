'''

'''

import numpy as np
import math
import recognize
import ezdxf

def print_entity(e):
    print("LINE on layer: %s\n" % e.dxf.layer)
    print(e.dxf.start)

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
	xMax,xMin,yMax,yMin = recognizeObject.getExtremePointInLines(xBigExWall)
	msp.add_line((xMax,yMin,0),(xMax,yMax,0))  # add a LINE entity
	xMax,xMin,yMax,yMin = recognizeObject.getExtremePointInLines(ySmallExWall)
	msp.add_line((xMin,yMin,0),(xMax,yMin,0))  # add a LINE entity
	xMax,xMin,yMax,yMin = recognizeObject.getExtremePointInLines(yBigExWall)
	msp.add_line((xMin,yMax,0),(xMax,yMax,0))  # add a LINE entity
	del recognizeObject

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

if __name__=="__main__":
	dwg = ezdxf.readfile("../../resources/QiangongF12010.dxf")
	msp = dwg.modelspace()
	recognizeBaseClass=recognize.__RecognizeBaseclass()

	xMax,xMin,yMax,yMin,xAvrg,yAvrg= recognizeBaseClass.getLinesAtributes(msp)
	print(xMax,xMin,yMax,yMin,xAvrg,yAvrg)

	
	dwg3 = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'
	msp3 = dwg3.modelspace()

	recognizeObjects=recognize.Recognize()
	xSmallExWall, xBigExWall, ySmallExWall, yBigExWall = recognizeObjects.sortExternalWall(xMax,xMin,yMax,yMin,msp)
	drawExWall(xSmallExWall, xBigExWall, ySmallExWall, yBigExWall, msp3)

	line = msp.query('LWPOLYLINE')
	pillarPlinesList = recognizeObjects.recognizeLWPolylinePillar(line,xMax,xMin,yMax,yMin)
	drawPillars(pillarPlinesList, msp3)

	dwg3.saveas('../../resources/line4.dxf')
