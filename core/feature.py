'''
This class aims at raising determinant features with various methods, such as correlation coefficient, Chi-square test
'''
from sklearn.tree import DecisionTreeClassifier
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





