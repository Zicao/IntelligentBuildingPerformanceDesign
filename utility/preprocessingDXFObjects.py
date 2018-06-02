'''
pre-processing the dxf file, for example, transform the polyline object to line object.
'''
from IntelligentBuildingPerformanceDesign.utility.line import Line
class preprocessingDXFObjects():
	'''

	'''
	def __init__(cls,*args,**kwargs):
		'''
		this class may receive different kinds of ezdxf objects, such as ezdxf Lines or Polylines.
		load the modelspace objects.
		for a multi-stories building, make sure the horizon plan are aligned to each other.
		'''
		isVerticalAlignedTrue=isVerticalAligned()
		if isVerticalAlignedTrue:
			pass
		else:
			pass
		pass
	def convertLWPolylinesIntoLines(self,msp,lines):
		'''
		convert the LWPolylines object in the ezdxf file into Line object. 
		When we say Line, it refers the Line object created in this module.
		The Line in ezdxf is called ezdxf Line.
		'''
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
		return lines
