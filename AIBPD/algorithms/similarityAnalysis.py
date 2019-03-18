#similarity analysis
'''

'''
import numpy as np
import pandas as pd
import re
from IntelligentBuildingPerformanceDesign.AIBPD.data.building import Building

class Similarity():
	
	buildingAttr4BN4CL=['ID','principleActivity','climateZone','buildingArea',\
							'yearOfConstruction','buildingShape',\
							'CDD65','COOLP','MAINCL','MAINHT',\
				             'wallConstruction', 'WWR',\
				             'MFCLBTU','EUICooling','HECS']
	buildingAttr4BN4CL_designer=['ID','climateZone','COOLP','principleActivity','MAINCL','HECS']		             
	def __init__(self):
		pass
	def similarityEuclidian(self, proposedDict, sampleDict, weight={'climateZone':3,
				'principleActivity':5,
				'buildingArea': 2,
				'yearOfConstruction':8,
				'buildingShape':2,
				'wallConstruction': 2,
				'WWR': 2,
				'peoplePerArea': 3}):
		'''
		Euclidian Distance is employed to calculate the similarity
		different features with different weight coefficient
		Diffence = weight(V1-V2)
		similarity = root (sum(squre(difference_i))) for i in features
		There are two types features in each piece(case) of data, i.e. continue, normal(categorical)

		Args:
			proposedDict, the proposed building.
			sampleDict, the sample building in the database.
			similarityItems, the items that used to calculate the similarity
			weight, the weight used to calculate similarity.

		Examples:
			prpsedBlding4SmlarAnalysis={'climateZone':3,
				'principleActivity':2,
				'buildingArea': 10000,
				'yearOfConstruction':1930,
				'buildingShape':2,
				'wallConstruction':2,
				'WWR': 0.3
				'peoplePerArea': 0.2}

			weight={'climateZone':3,
				'principleActivity':2,
				'buildingArea': 2,
				'yearOfConstruction':2,
				'buildingShape':2,
				'wallConstruction': 2,
				'WWR': 2,
				'peoplePerArea': 3}
		'''
		itemDict=proposedDict.keys()
		similarValue = 0.0
		for i in itemDict:
			#nomial variable (categorical variable)
			if re.search(i,'climateZone principleActivity wallConstruction buildingShape',re.I):
				if proposedDict[i]==sampleDict[i]:
					similarValue+=weight[i]**2
			#continue variable
			if re.search(i,'buildingArea yearOfConstruction WWR peoplePerArea',re.I):
				diffPercentage=abs(proposedDict[i]-sampleDict[i])/proposedDict[i]
				similarValue+=self.calculateValue(diffPercentage,weight[i])**2
		return similarValue

	def calculateValue(self,difPercentage, maxValue):
		simValue = maxValue*(1-difPercentage)
		return simValue

	def kSimilarBuildings(self, proposedBuilding, databaseDF, K=300):
		'''
		return K most similar building
		Args:
			proposedBuilding, a dict object used to describe the building.
			databaseDF, a pandas DataFrame object.
			K, an integral.
		Return:
			A list of indices of these K buildings
		'''
		prpsedBlding4SmlarAnalysis=proposedBuilding.blding4SimilarityAnalysis()
		EuclidianDistance=[]
		m,n=databaseDF.shape
		keys=prpsedBlding4SmlarAnalysis.keys()
		databaseDF=databaseDF.reindex(range(databaseDF.shape[0]))
		for index, row in databaseDF.iterrows():
			sampleBlding={}
			for key in keys:
				sampleBlding[key]=row[key]
			EuclidianDistance.append(self.similarityEuclidian(prpsedBlding4SmlarAnalysis,sampleBlding))

		indices = np.lexsort(np.array([EuclidianDistance]))
		indices = indices.tolist()

		similarBuildingsDict={}

		for i in self.buildingAttr4BN4CL:
			similarBuildingsDict[i]=[]

		for i in indices[0:K]:
			for item in self.buildingAttr4BN4CL:
				similarBuildingsDict[item].append(databaseDF[item].loc[i])
		similarBuildingsDF=pd.DataFrame(similarBuildingsDict)
		return similarBuildingsDF
	def subDF(self, databaseDF):
		'''
		return subset of databaseDF only for building a Bayesian Network model 
		'''
		return databaseDF[self.buildingAttr4BN4CL]

			