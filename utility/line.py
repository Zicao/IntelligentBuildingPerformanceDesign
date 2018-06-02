'''
This class is used to transfer all kinds of ezdxf entity, such as lines and polyline
'''
import math
from IntelligentBuildingPerformanceDesign.utility.point import Point

class Line():

	
	def __init__(cls, p1, p2):
		'''
		Args:
			p1 and p2 are two Point object defined in point.py

		Attributes:
			p1X, p1Y are the (x,y) value of first point (p1)
			p2X, p2Y are the (x,y) value of the second point(p1)
		'''
		cls.p1=Point(p1)
		cls.p2=Point(p2)
		cls.p1X=cls.p1.X
		cls.p1Y=cls.p1.Y

		cls.p2X=cls.p2.X
		cls.p2Y=cls.p2.Y
		if p1==p2:
			raise ValueError(
                "%s.__new__ requires two unique Points." % cls.__name__)
		
	def slope(self):
		'''
		calculate the slope of this line or infinite if vertical.
		'''
		if self.p1X==self.p2X:
			return math.inf
		else:
			return (self.p2Y-self.p1Y)/(self.p2X-self.p1X)

	def length(self):
		'''
		Eulidian distance between two point of this line.
		'''
		return self.p1.distance(self.p2)#math.sqrt((p1X-p2X)**2+(p1Y-p2Y)**2)
	def isParallel(self,l1):
		'''
		judge whether l1 parallel to self.
		'''
		if type(l1)==type(self):
			if self.slope()==l1.slope():
				return True
			else:
				return False
		else:
			raise(TypeError)
			#print(e.message)
	def distance(self,point1):
		'''
		calculate the distance between a point1 and this line
		Args:
			point1, a Point object.
		'''
		if self.slope()!=math.inf and self.slope()!=0:
			#line dont vertical to X axis.
			point0=Point()
			if point1.Y-self.slope()*(point1.X-self.p1X)-self.p1Y==0:
				return 0
			else:
				#the line: y=slope*(x-self.p1X)+self.p1Y
				#line vertical to self(line): y=(1/slope)*(x-point1.X)+point1.Y
				#interaction point0 of these two line is 
				#point0.X=(self.p1Y-point1.Y)-((1/slope)*point1.X-slope*self.p1X)/(1/slope-slope)
				a=self.slope()
				c=-1/a
				b=self.p1Y-a*self.p1X
				d=point1.Y-c*point1.X
				point0.X=(d-b)/(a-c)
				point0.Y=c*point0.X+d
				return point0.distance(point1)
		elif self.slope()==math.inf:
			#vertical to the x axis
			return math.fabs(self.p1X-point1.X)
		elif self.slope()==0:
			return math.fabs(self.p1Y-point1.Y)
		else:
			print("Errors occured")
	def isVertical(self,line1):
		'''
		judge whether line1 parallel to line(self) or not
		Args:
			line1, a Line object
		'''
		if self.slope()==math.inf:
			if line1.slope()==0:
				return True
			else:
				return False
		elif self.slope()==0:
			if line1.slope()==math.inf:
				return True
			else:
				return False
		else:
			if self.slope()*line1.slope()==-1:
				return True
			else:
				return False


if __name__=="__main__":
	line1=Line((0,0),(0,1))
	line2=Line((0,2),(1,3))
	slope1=line1.slope()
	slope2=line2.slope()
	print(slope1)
	print(slope2)
	parallel=line1.isParallel(line2)
	print(parallel)
	point1=Point((0,4))
	print(line1.distance(point1))