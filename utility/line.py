
'''
This class is used to transfer all kinds of ezdxf entity, such as lines and polyline
'''
import math
import numpy as np
from aibpd.utility.point import Point

class Line():
	rho=0.0
	theta=0.0
	length=0.0
	midpoint=Point((0,0))
	a=0.0
	b=0.0
	c=1.0
	__name__='Line'
	def __init__(self, p1, p2,endPoint1=None,endPoint2=None,a=None,b=None,c=None):
		'''
		Args:
			p1 and p2 are two Point object defined in point.py
			ax+by=c
		Attributes:
			p1X, p1Y are the (x,y) value of first point (p1)
			p2X, p2Y are the (x,y) value of the second point(p1)

		'''
		if  endPoint1 and  endPoint2:
			self.p1=endPoint1
			self.p2=endPoint2
		else:
			self.p1=Point(p1)
			self.p2=Point(p2)
		self.p1X=self.p1.X
		self.p1Y=self.p1.Y

		self.p2X=self.p2.X
		self.p2Y=self.p2.Y
		if p1==p2:
			raise ValueError("%s.__new__ requires two unique Points." % self.__name__)
		if self.p1X==self.p2X:
			self.theta=np.pi/2
		else:
			self.theta=math.atan(abs((self.p2Y-self.p1Y)/(self.p2X-self.p1X)))

		pointMatrix=np.mat(([[self.p1X,self.p1Y],[self.p2X,self.p2Y]]))

		if not a:
			if np.linalg.det(pointMatrix)==0:
				if self.p1X==self.p2X and self.p1X!=0:
					self.a=1.0/self.p1X
					self.b=0.0
				elif self.p1X==self.p2X and self.p1X==0:
					self.a=1.0
					self.b=0.0
					self.c=0.0
				elif self.p1Y==self.p2Y and self.p1Y!=0:
					self.a=0.0
					self.b=1.0/self.p1Y
				elif self.p1Y==self.p2Y and self.p1Y==0:
					self.a=0.0
					self.b=1.0
					self.c=0.0
				elif self.p1X==0 and self.p1Y==0:
					self.c=0.0
					if self.p2X!=0:
						a=-self.p2Y/self.p2X
						self.b=1.0
					else:
						self.a=1.0
						self.b=0
				elif self.p2X==0 and self.p2Y==0:
					self.c==0.0
					if self.p1X!=0:
						a=-self.p1y/self.p1X
						self.b=1.0
					else:
						self.a=1.0
						self.b=0

			else:
				self.c=1.0
				self.a=(pointMatrix.I*np.mat([[1],[1]]))[0,0]
				self.b=(pointMatrix.I*np.mat([[1],[1]]))[1,0]
			print('a',self.a,'b',self.b,'c',self.c)
		else:
			self.a=a
			if b:
				self.b=b
			else:
				print('b is not given')
			if c:
				self.c=c
			else:
				print('c is not given')
		self.length=self.p1.distance(self.p2)
		self.midpoint=Point(((self.p1X+self.p2X)/2,(self.p1Y+self.p2Y)/2))
		
	def slope(self):
		'''
		calculate the slope of this line or infinite if vertical.
		'''
		if self.p1X==self.p2X:
			return float('inf')
		else:
			return (self.p2Y-self.p1Y)/(self.p2X-self.p1X)

	def length(self):
		'''
		Eulidian distance between two point of this line.
		'''
		return self.p1.distance(self.p2)#math.sqrt((p1X-p2X)**2+(p1Y-p2Y)**2)
	def isParallel(self,l1):
		'''
		judge whether l1 parallel to this object.
		'''
		if type(l1)==type(self):
			if self.slope()==l1.slope():
				return True
			else:
				return False
		else:
			raise(TypeError)
			#print(e.message)
	def isAlmostParallel(self,l1,deltaTheta=np.pi/72):
		'''
		judge whether l1 almost parallel to this object.
		Args:
			l1 another line.
			deltaTheta, the max limitation of angles between this two lines. 
				pi=3.14,pi/2=1.52, pi/6=0.52, pi/18=0.174 (10 degree), pi/36=0.087
		Example:
			line1=Line((0,0),(0,1))
			line2=Line((0.1,0.1),(0,1))
			slope1=line1.slope()
			slope2=line2.slope()
			print("Is line1 and line2 parallel?",line1.isParallel(line2))
			print("Is line1 and line2 parallel?",line1.isAlmostParallel(line2,0.2))

			Output:
				('Is line1 and line2 parallel?', False)
				('Is line1 and line2 parallel?', True)
		'''
		if type(l1)==type(self):
			if abs(self.theta-l1.theta)<=deltaTheta:
				return True
			else:
				return False
		else:
			raise(TypeError)


	def distance(self,point1):
		'''
		calculate the distance between a point1 and this line
		Args:
			point1, a Point object.
		'''
		if self.slope()!=float('inf') and self.slope()!=0:
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
		elif self.slope()==float('inf'):
			#vertical to the x axis
			return math.fabs(self.p1X-point1.X)
		elif self.slope()==0:
			return math.fabs(self.p1Y-point1.Y)
		else:
			print("Errors occured")

	def distanceOfParallelLines(self,line1,deltaDis):
		'''
		Judge whether the distance between two parallel lines small than deltaDis.
		So first of all, this function judge whether these two lines are parallel mutually.
		Args:
			line1, anther line that paralleled to self.
			deltaDis, the maximum distance.
		'''
		if self.isAlmostParallel(line1,np.pi/50) and self.distance(line1.p1)<=deltaDis and self.distance(line1.p2)<=deltaDis:
			return True
		else:
			return False

	def isVertical(self,line1):
		'''
		judge whether line1 parallel to line(self) or not
		Args:
			line1, a Line object
		'''
		if self.slope()==float('inf'):
			if line1.slope()==0:
				return True
			else:
				return False
		elif self.slope()==0:
			if line1.slope()==float('inf'):
				return True
			else:
				return False
		else:
			if self.slope()*line1.slope()==-1:
				return True
			else:
				return False
	def interactedPointofTwoLines(self,line1):
		'''
		get the interacted point of two lines which are unparallel to each other.
		Args:
			line1, a Line object.
		'''
		x=None
		y=None
		interactedPoint=Point()
		if self.isAlmostParallel(line1):
			#raise("These two lines are paralleled to each other.")
			endp1=Point()
			for p in [line1.p1,line1.p2]:
				if p.distance(self.midpoint)>self.length/2:#more exactly, cos(distanceOfP2midpoint)
					endp1=p
			vertical2Line1=Line()
			vertical2Line1.c=self.b*endp1.x-self.a*endp1.y
			vertical2Line1.a=self.b
			vertical2Line1.b=-self.a

			pointMatrix=np.mat(([[self.a,self.b],[vertical2Line1.a,vertical2Line1.b]]))
			matrixC=np.mat([[self.c],[vertical2Line1.c]])
			
			
			x=(pointMatrix.I*matrixC)[0,0]
			y=(pointMatrix.I*matrixC)[1,0]
			interactedPoint.x=x
			interactedPoint.y=y
		else:
			def lineInteraction(line1,line2):
				xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
				ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])
				def det(a, b):
					return a[0] * b[1] - a[1] * b[0]

				div = det(xdiff, ydiff)
				if div == 0:
					raise Exception('lines do not intersect')

				d = (det(*line1), det(*line2))
				x = det(d, xdiff) / div
				y = det(d, ydiff) / div
				return x,y
			x,y=lineInteraction(((self.p1.x,self.p1.y),(self.p2.x,self.p2.y)),((line1.p1.x,line1.p1.y),(line1.p2.x,line1.p2.y)))
			interactedPoint.x=x
			interactedPoint.y=y
		return interactedPoint

if __name__=="__main__":
	line1=Line((0,0),(1,1))
	line2=Line((0.1,0.1),(0,1))
	line3=Line((0,10),(1,11))
	line4=Line((0,10),(2,12))


	slope1=line1.slope()
	slope2=line2.slope()
	print("Is line1 and line2 parallel?",line1.isParallel(line2))
	print("Is line1 and line2 parallel?",line1.isAlmostParallel(line2,0.2))
	interPoint=line3.interactedPointofTwoLines(line1)
	print('interactedPoint',interPoint.x,interPoint.y)

	print('a b of line1',line1.a,line1.b)
	print('midpoint of line1',line1.midpoint.x,line1.midpoint.y)
	print('exetend line',line1.interactedPointofTwoLines(line4).x,line1.interactedPointofTwoLines(line4).y)
	line4=Line()