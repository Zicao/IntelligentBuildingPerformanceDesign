'''
This class aims at raising determinant features with various methods, such as correlation coefficient, Chi-square test
'''
from sklearn.tree import DecisionTreeClassifier
from sets import Set
class BaseFeature():
	"""

	"""
	def __init__(self):
		pass

	def featureRanking(self,method=None):
		"""
		define the feature ranking method
		"""

class FeatureRanking(BaseFeature):
	"""rank building features with statistical methods, such as Pearson
	Coorelation Coefficient, and ANOVA.

	Parameters:
	---------
	datasetDF, the dataset.
	YFeature, the dependant feature.
		For example, EUI, or HEUI
	rankM, ranking methods. You can choose one method or 'all' method, 
		or a list methods. candidate methods include 'corr' (correlation
		coefficient), 'AVOVA' (Analysis of Variance).
	
	Return:
	----------


	"""
	
	def __init__(self,datasetDF,YFeature='EUI',rankM=None):
		self.datasetDF=datasetDF
		self.YFeature=YFeature
		self.rankM=rankM

	def rank(self):
		"""

		"""
		pass

	def corr(self):
		"""rank feature using Pearson Correlation Coefficient.

		"""
		corrDF=self.datasetDF.corr()
		corrValue=corrDF[self.YFeature]
		columns=datasetDF.columns
		#sort the numbers
		sortedIndex=np.lexsort((columns,corrValue))
    	return [(columns[i],corrValue[i]) for i in sortedIndex]

    def chisquare(self):
    	"""rank feature using chi
    	"""
    	pass

    def SHAP(self):
    	"""
    	rank features using SHAP methods.
    	"""
    	pass

    def featureDistribution(self,database,YName='heatingLevel'):
    	"""demonstrate the feature distribution in high and low performance building
    	groups.

    	Parameters:
    	---------
    	database, the Database object.
    	YName, the target variable name.

    	Return:
    	--------
    	
    	"""
    	#test the Y-value variable are 0 or 1
    	datasetDF_HP=None
    	datasetDF_LP=None
    	datasetDF=database._datasetDF
		if YName in datasetDF.columns:
			observations = Set(list(datasetDF[YName].values))
			if len(observations)<=5 and Set([0,1]).issubset(observations):
				datasetDF_HP=datasetDF[datasetDF[YName]>0][datasetDF[YName]<=1]
				datasetDF_LP=datasetDF[datasetDF[YName]>=0][datasetDF[YName]<1]
				#print the P-value of all features for categorical data
			else:
				print('The target variable Y is not a categorical variable!')
				return
		else:
			print(YName, 'is not a column of the dataset')
			return

		#Print all the P-value of the chi-square test for categical feature.
		for featureName in database.categoricalFeatureList:
			feature_high=dict(Counter(datasetDF_HP[featureName]))
			feature_low=dict(Counter(datasetDF_LP[featureName]))
			list1=[]
			list2=[]
			for i in feature_high.keys():
				if i in feature_low.keys():
					list1.append(feature_high[i])
					list2.append(feature_low[i])
			chisq,pvalue=chisquare(list1,list2)
			print('Chi-square test, p-value',featureName,'=',pvalue)


    	



class FeatureWrapper(BaseFeature):
	"""select feature with wrapper methods. The machine learning methods
	can be decision tree, gini index etc.
	
	Parameters:
	-----------

	Return:
	----------

	"""
	def __init__(self,datasetDF,YFeature='EUI',rankM=None):
		pass

	def stepforward(self,featureList=None,targetFeatureName='EUI'):
		"""raise the best features.
		"""
		pass

	def decisiontree(self, featureList=None, targetFeatureName='EUI'):
    	"""find out determine feature with information gain.
    	Parameters:
    	----------
    	featureList, a list of candidate features that may influence the 
    		building performance. It is recommended that a feature selection 
    		process using step forward wrapper methods.
    	Return:

    	Examples:
    	----------

    	Reference:
    	
    	"""
    	#list features based on their entropy loss.

    	#draw the whole tree structure.





