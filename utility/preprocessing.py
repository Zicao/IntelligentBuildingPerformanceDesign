'''
This class is used to pre-processing data for different goals, for example similarity analysis
'''
import numpy as np

class Preprocessing(caseMat):
	
	def __init__(self):
	
		pass;
	def cleaning(self):
	
		pass;
	def mapping(self):
		
		pass;
	def fillLostValue(caseMat):
	#miss value will be filled with -1
		m,n = caseMat.shape
		caseList = []
		for i in range(n):
			v1=str(caseMat[0,i])
			if not v1.strip():
				v1 = '-1'
			caseList.append(float(v1))
		return caseList
	