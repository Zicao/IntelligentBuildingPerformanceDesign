#similarity analysis
'''

'''
import numpy as np

class Similarity():
	
	
	def __init__(self):
	
	def similarity(baseCaseMat, referCaseMat, itemList, weight):
	'''
	#Euclidian Distance is employed to calculate the similarity
	#different items with different weight coefficient
	#Diffence = weight(V1-V2)
	#similarity = root (sum(squre(differencei))) for i in items
	#There are two types features in each piece(case) of data, i.e. continue, normal(categorical)
	'''
		simPoints = 0
		baseCaseList,referCaseList = preProcessing(baseCaseMat,referCaseMat)
		baseCaseMatrix = np.mat(baseCaseList)
		referCaseMatrix = np.mat(referCaseList)
		
		for i in itemList:
			
			#Principal building activity
			if i==4 or i==12:
				if baseCaseMatrix[0,i-1]==referCaseMatrix[0,i-1]:
					simPoints += 5**2
			#Square footage category
			elif i==7 or i==25 or i==94:
				difPercentage = abs(baseCaseMatrix[0,i-1]-referCaseMatrix[0,i-1])/10
				simPoints = getPoints(difPercentage,10,-10)**2+simPoints
			elif i==8 or i==13:
				difPercentage = abs(baseCaseMatrix[0,i-1]-referCaseMatrix[0,i-1])/5
				simPoints += getPoints(difPercentage, 5, -5)**2
			elif i == 1119:
				difPercentage = abs(baseCaseMatrix[0,i-1]-referCaseMatrix[0,i-1])/5
				simPoints += getPoints(difPercentage, 10, -10)**2
			else:
				print("similar calcu error")
		return simPoints