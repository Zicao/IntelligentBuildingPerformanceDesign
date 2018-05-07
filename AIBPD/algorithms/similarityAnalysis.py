#similarity analysis
'''

'''
import numpy as np
import ...utility import preProcessing

class Similarity():
	
	
	def __init__(self):
	
	def similarity(self, caseMat, sampleMat, itmIndxN, itmIndxC, weight):
	'''
	#Euclidian Distance is employed to calculate the similarity
	#different features with different weight coefficient
	#Diffence = weight(V1-V2)
	#similarity = root (sum(squre(difference_i))) for i in features
	#There are two types features in each piece(case) of data, i.e. continue, normal(categorical)
	'''
		simPoints = 0.0
		#caseList,sampleList = preProcessing.fillLostValue(caseMat, sampleMat)
		caseMat = np.mat(caseList)
		sampleMat = np.mat(sampleList)
		similarValue = 0.0
		similarValue = similarityNormal(self, caseMat, sampleMat, itmIndxN, weight) + similarityContinuous(self, caseMat, sampleMat, itmIndxC, weight)
				
		return similarValue
	def similarityNormal(self, caseMat, sampleMat, itmIndxN, weight):
		'''
		
		'''
		similarValue = 0.0
		for i in itmIndxN:
			if caseMat[0,i-1]==sampleMat[0,i-1]:
				similarValue+=weight[i]
		return similarValue
	def similarityContinuous(self, caseMat, sampleMat, itmIndxC, weight):
		'''
		
		'''
		similarValue = 0.0
		for i in itmIndxC:
			difference=abs(caseMat[0,i-1]-sampleMat[0,i-1])
			difference=1/exp(difference)
			similarValue += weight[i] * difference
		return similarValue
		