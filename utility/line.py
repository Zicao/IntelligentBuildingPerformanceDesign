'''
This class is used to transfer all kinds of ezdxf entity, such as lines and polyline
'''
import math
from .point import Point
class Line():

	def __init__(cls,p1,p2):
		p1S,p1E=p1
		p2S,p2E=p2
		if p1==p2:
			raise ValueError(
                "%s.__new__ requires two unique Points." % cls.__name__)
		
	def length(self):
		L=math.sqrt()
		return math.sqrt((p1S-p2S)^2+(p1E+p2E)^2)
