#similarity analysis
'''

'''
import numpy as np
import pandas as pd
import re
from aibpd.data.building import Building

class BaseSimilarity():
	'''
	Base class for similarity classes
	This class should not be used directly.	
	'''
	featureAndweightDict={'climateZone':3,
				'principleActivity':5,
				'buildingArea': 2,
				'yearOfConstruction':8,
				'buildingShape':2,
				'wallConstruction': 2,
				'WWR': 2}

	def __init__(self):
		pass

	def setFeatures(self,featureAndweightDict=None):
		'''
		set which features should be used to calculate similarity.
		'''
		#set check mechanism to make sure these features coincide with feature in Buildings.
		#it's better to set up a CONSTANT standard feature list.
		self.featureAndweightDict=featureAndweightDict


class SimilarityKmeans(BaseSimilarity):
	'''
	Find similar buildings using the k-means algorithm.
	'''
	def __init__(self,):

		pass

class SimilarityEuclidian(BaseSimilarity):
	'''
	Find out buildings that are similar to the design building with Euclidian distance.
	Args:
		designBuilding
			the design building. Data type: Building;
		databaseDF
			the database based on which conduct the similar analysis. Data type: DataFrame.
		featureAndweightDict
			contains the features used to calculate the similarity and their weights. Data type: dict.
		k:
			number of buildings.
	'''
	
	buildingAttr4BN4CL_designer=['ID','climateZone','COOLP','principleActivity','MAINCL','HECS']		             
	
	def __init__(self):
		pass

	def euclidianDistance(self, proposedDict, sampleDict):
		'''
		Euclidian Distance is employed to calculate the similarity
		different features with different weight coefficient
		Diffence = weight(V1-V2)
		similarity = root (sum(squre(difference_i))) for i in features
		There are two types features in each piece(case) of data, i.e. continue, normal(categorical)

		Args:
			proposedDict:
				the proposed building.
			sampleDict:
				the sample building in the database.

		'''
		featureAndweightDict=self.featureAndweightDict
		itemDict=featureAndweightDict.keys()
		similarValue = 0.0
		for i in itemDict:
			#nomial variable (categorical variable)
			if re.search(i,'climateZone principleActivity wallConstruction buildingShape',re.I):
				if proposedDict[i]==sampleDict[i]:
					similarValue+=featureAndweightDict[i]**2
			#continue variable
			if re.search(i,'buildingArea yearOfConstruction WWR peoplePerArea',re.I):
				diffPercentage=abs(proposedDict[i]-sampleDict[i])/proposedDict[i]
				similarValue+=self.calculateValue(diffPercentage,featureAndweightDict[i])**2
		return similarValue

	def calculateValue(self, difPercentage, maxValue):
		simValue = maxValue*(1-difPercentage)
		return simValue

	def get(self,designBld=None, databaseDF=None,K=300):
		'''
		return K most similar building
		Args:
			designBld, a dict object used to describe the building.
			databaseDF, a pandas DataFrame object.
			K, an integral.
		Return:
			similar buildings in the 
		'''
		

		featuresWithWeight=self.featureAndweightDict
		EuclidianDistance=[]
		m,n=databaseDF.shape
		keys=featuresWithWeight.keys()

		for index, row in databaseDF.iterrows():
			sampleBlding={}
			for key in keys:
				sampleBlding[key]=row[key]
			EuclidianDistance.append(self.euclidianDistance(featuresWithWeight,sampleBlding))

		indices = np.lexsort(np.array([EuclidianDistance]))
		indices = indices.tolist()
		return databaseDF.iloc[indices]

	def subDF(self, databaseDF):
		'''
		return subset of databaseDF only for building a Bayesian Network model 
		'''
		return databaseDF[self.buildingAttr4BN4CL]


			