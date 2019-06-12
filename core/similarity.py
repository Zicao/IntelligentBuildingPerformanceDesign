#similarity analysis
import numpy as np
import pandas as pd
import re
from aibpd.data.building import Building
from aibpd.data.database import Database
from sklearn.preprocessing import MinMaxScaler
import math
__all__=['get_ksimilar']

feature_weights={'climateZone':3,
			'principleActivity':5,
			'buildingAreaCategory': 2,
			'yrConstructionCategory':8,
			'buildingShape':2,
			'wallConstruction': 2,
			'WWR': 2}
buildingAttr4BN4CL_designer=['ID','climateZone','COOLP','principleActivity','MAINCL','HECS']


def get_ksimilar(database=None, building = None, K=300, feature_weights=None, method='Euc'):
	'''
	return K most similar building
	Args:
		designBld, a dict object used to describe the building.
		dataDF, a pandas DataFrame object.
		K, an integral.
	Return:
		similar buildings in the 
	'''
	
	if method=='Euc':
		return get_ksimilar_Euclidian(database._dataDF, building._data, K, feature_weights)
	else:
		return None

def get_ksimilar_Euclidian(dataDF=None, building=None, K=300, feature_weights=None):
	"""find out k similar building for the design building with Euclidian distance
	"""
	euclidian_distance=[]
	keys=list(feature_weights.keys())
	#max_min preprocessing for numeric features
	databaseDF=dataDF[keys]
	for index, sample_building in databaseDF.iterrows():
		euclidian_distance.append(get_euclidian_distance(building,sample_building,feature_weights))
	dataDF['similarity']=euclidian_distance
	indices = np.lexsort(np.array([euclidian_distance]))
	indices = indices.tolist()
	indices = indices[-K:]
	return Database(dataDF=dataDF.iloc[indices])

def get_euclidian_distance(building, sample_building, feature_weights=None):
	'''
	Euclidian Distance is employed to calculate the similarity
	different features with different weight coefficient
	Diffence = weight(V1-V2)
	similarity = root (sum(squre(difference_i))) for i in features
	There are two types features in each piece(case) of data, i.e. continue, normal(categorical)

	Args:
		building:
			the proposed building.
		sample_building:
			the sample building in the database.

	'''
	keys=feature_weights.keys()
	similarValue = 0.0
	for i in keys:
		#categorical variable (categorical variable)
		if i in Database.main_feature_categorical:
			if building[i]==sample_building[i]:
				similarValue+=feature_weights[i]**2
		#numeric variable
		elif i in Database.main_feature_numeric:
			#re.search(i,'buildingArea yearOfConstruction WWR peoplePerArea',re.I)
			diffPercentage=abs(building[i]-sample_building[i])
			similarValue+=feature_diff(diffPercentage,feature_weights[i])**2
	return math.sqrt(similarValue)

def feature_diff(difPercentage, weight):
	"""calculate the difference of a continuous feature in two buildings.
	Parameters:
	------------
	diff_ratio, the difference ratio of a feature in two sample buildings.
	weight, the weight of a feature.
	
	Return:
	----------
	the feature similarity of a feature in two buildings.
	"""

	simValue = weight*(1-difPercentage)
	return simValue


	
def set_weights(feature_weights):
	"""set the weights of the features.

	Parameters
	----------
	feature_weights, a dict that contains the weights of different features.
	Return:
	----------
	None
	"""
	feature_weights=feature_weights

def subDF(dataDF):
	'''
	return subset of dataDF only for building a Bayesian Network model 
	'''
	return dataDF[buildingAttr4BN4CL]