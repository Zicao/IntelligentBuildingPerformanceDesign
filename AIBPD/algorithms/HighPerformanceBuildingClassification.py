#Predict whether a building is high performance or not using machine learning algorithms such as desicion tree and svm
from IntelligentBuildingPerformanceDesign.AIBPD.data.preprocessing import PreprocessingCBECS
from IntelligentBuildingPerformanceDesign.AIBPD.data.database import Database
import numpy as np
from sklearn import tree
class HPBClf():
	def __init__(self,X,Y):
		'''
		Attributes:
			X, the attributes 
			Y, values
		'''
		pass
class DT4Clf(HPBClf):
	
	def __init__(self,X,Y):
		pass

	def fit(X,Y):
		'''
		X, data
		Y, target
		'''
		clf=tree.DecisionTreeClassifier()
		clf.fit(X,Y)
if __name__ == '__main__':
	database=Database()
	CBECS_DF=database.select('CBECS2012')
	Preproc=PreprocessingCBECS(CBECS_DF)
	CBECS_DF=Preproc.forHEHSClf(CBECS_DF)
	X=CBECS_DF[['censusRegion','principleActivity','numPeoplePerAreaCate','wallConstruction','WWR','numFloors',#
				'yrConstructionCategory','insulationUpgrade',\
				#'ELHT1','NGHT1','STHT1','HWHT1',\buildingAreaCategory
				'MAINHT']].values
	#ELHT1:Electricity used for main heating
	#STHT1:District steam used for main heating
	#HWHT1:District hot water used for main heating
	#MAINHT:Main heating equipment
	Y=CBECS_DF['HEHS'].values
	HP=CBECS_DF[CBECS_DF['HEHS']==1.0]
	MP=CBECS_DF[CBECS_DF['HEHS']==2.0]
	LP=CBECS_DF[CBECS_DF['HEHS']==3.0]
	CBECS_DF=Preproc.forHECSClf(CBECS_DF)

	CBECS_DF=Preproc.forHEEBClf(CBECS_DF)

	print(CBECS_DF['EUIHeating'].mean(),CBECS_DF['EUIHeating'].std())
	print(CBECS_DF['EUICooling'].mean(),CBECS_DF['EUICooling'].std())
	print(CBECS_DF['EUI'].mean(),CBECS_DF['EUI'].std())
	CBECS_DF['EUI'].hist(bins=20)