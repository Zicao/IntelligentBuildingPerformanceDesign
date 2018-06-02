'''

'''
import math
class Point():
	'''
	Example:
	point1=Point((0,0)).
	At this time Point(0,0) doesnot work.
	'''
	def __init__(cls,XY=(0,0)):
		cls.X,cls.Y=XY[0],XY[1] #(X,Y) is the coordinates of this point
		cls.x,cls.y=XY[0],XY[1] #someone may like to use (x,y)

	def distance(self,point1):
		'''
		return Eulidian distance
		'''
		return math.sqrt((self.X-point1.X)**2+(self.Y-point1.Y)**2)
	def  __and__(self,point1):
		x = self.x + point1.x
		y = self.y + point1.y
		return Point(x,y)
