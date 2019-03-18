
import numpy as np
import pandas as pd

from IntelligentBuildingPerformanceDesign.AIBPD.data.building import Building
from sklearn.preprocessing import Imputer
from IntelligentBuildingPerformanceDesign.AIBPD.data.weather import Weather
class Preprocessing():
	'''
	This class is used to pre-processing data for different goals, for example similarity analysis
	'''
	def __init__(self):
		#self.m,self.n = dataDF.shape
		#self.checkKeywords(dataDF,Building)
		#self.fillValue(dataDF)
		pass

	def cleaning(self,dataDF):
		
		pass;
	def mapping(self,dataDF):
		
		pass;

	def fillValue(self,dataDF):
		'''
		fill none with Value 0
		Return:
			post processed dataDF object
		'''
		dataDF.fillna(0, inplace=True)
	def deleteDuplicated(self,dataDF):
		'''
		Delete duplicated objects in the database()
		Args:
			dataDF, a DataFrame object that contain all the data of the database.
		'''
		dataDF=dataDF.drop_duplicates()

	def checkKeywords(self,dataDF,Building):
		'''
		Check whether the names of attributes coincide names defined in Building class, i.e. Building.building.keys()
		Args:
			dataDF, a DataFrame object that contain all the data of the database.
			building, a Building object.
		'''
		buildingAttribute=Building.building.keys()
		if buildingAttribute:
			for i in dataDF.columns:
				if i not in buildingAttribute:
					print('Please check name of',i,'which does not coincide attributes in your database')

	def getHP(self, dataDF, energyType=None):
		'''
		Judge whether a building are high performance or not.
		Args:
			dataDF:
			energyType: different energy consumption items, such annual energy usage intensive(EUI).
						0= 'EUI', => 'HEEB'= high energy efficient building
						1='EUIHeating' => 'HEHS'= high efficient heating system
						2='EUICooling' => 'HECS' = high efficient cooling system
						3='designHeatingLoad' => 'HEE4H' = high efficient envelop system for heating.
						4='designCoolingLoad' => 'HEE4C' = high efficient envelop system for cooling.
		'''
		
		try:
			#energyTypeDict={0:'EUI',1:'EUIHeating',2:'EUICooling',3:'designHeatingLoad',4:'designCoolingLoad'}
			highEfficientType={'EUI': 'HEEB','EUIHeating': 'HEHS','EUICooling': 'HECS','designHeatingLoad':'HEE4H',
								'designCoolingLoad':'HEE4C',
								'SourceEUI':'HEEB'}
			#energyName=energyTypeDict[energyType]
			isHEName=highEfficientType[energyType]
		except:
			energyName='EUI'
			isHEName='HEEB'
		#dataDF=dataDF[dataDF[energyType]>0]
		print('dataDF in preprocessing shape',dataDF.shape)
		top3=dataDF[energyType].sort_values().iloc[int(0.03*dataDF.shape[0])]
		top23=dataDF[energyType].sort_values().iloc[int(0.23*dataDF.shape[0])]
		top10=dataDF[energyType].sort_values().iloc[int(0.10*dataDF.shape[0])]
		top25=dataDF[energyType].sort_values().iloc[int(0.25*dataDF.shape[0])]
		top75=dataDF[energyType].sort_values().iloc[int(0.75*dataDF.shape[0])]
		top90=dataDF[energyType].sort_values().iloc[int(0.90*dataDF.shape[0])]
		hpcsList=np.zeros((dataDF.shape[0]))
		print('top3',top3,'top10',top10,'top23',top23,'top25',top25,'top75',top75,'top90',top90)
		dataDF=dataDF.reindex(range(dataDF.shape[0]))
		for i in range(dataDF.shape[0]):
			if dataDF[energyType].iloc[i]<=top23 and dataDF[energyType].iloc[i]>top3:
				hpcsList[i]=1.0
			elif dataDF[energyType].iloc[i]<=top75 and dataDF[energyType].iloc[i]>top25:
				hpcsList[i]=2.0
			elif dataDF[energyType].iloc[i]<=top90 and dataDF[energyType].iloc[i]>top75:
				hpcsList[i]=0.0
			else:
				hpcsList[i]=3.0
		dataDF[isHEName]=pd.Series(hpcsList)
		del hpcsList
		return dataDF


	def addweatherData(self,dataDF):
		'''
		add weather data in to dataDF by city name.
		'''
		Weather.addWeatherAttributesIntoDataDFByCity(dataDF)

class PreprocessingCBECS(Preprocessing):

	def __init__(self):
		#self.m,self.n = dataDF.shape
		#self.fillValue(dataDF)
		pass


	def getEUICooling(self,dataDF):
		'''
		calculate source energy usage intension for cooling. 
		Args:
			dataDF, the source data based on which the EUICooling is calculated.
		'''
		#dataDF['EUICooling']=(dataDF['ELCLBTU']*3.167+dataDF['NGCLBTU']*1.084\
								#+dataDF['DHCLBTU']*3.613+dataDF['FKCLBTU']*1.05)/dataDF['buildingArea']

		dataDF['EUICooling']=dataDF['MFCLBTU']/dataDF['buildingArea']


	def getEUIHeating(self,dataDF):
		'''
		calculate sources energy usage intension for heating
		'''
		dataDF['EUIHeating']=dataDF['MFHTBTU']/dataDF['buildingArea']
		return dataDF[dataDF['EUIHeating']>=0][dataDF['EUIHeating']<=1000]

	def getHECS(self,dataDF):
		'''
		Buildings with the least EUICooling are sorted out. To increase credility, top 3% low 
		cooling energy buildings are abandoned. This low cooilng energy buildings are call High Efficient
		Cooling System (HECS).
		Args:
			dataDF, the source data based on which the EUIHeating is calculated.	
		'''
		self.getHP(dataDF, energyType='EUICooling')
	def getHEES(self,dataDF):
		'''

		'''
		self.getHP(dataDF, energyType='EUI')

	def getHEHS(self,dataDF):
		'''

		'''
		return self.getHP(dataDF, energyType='EUIHeating')

	def getEUI(self,dataDF):
		'''
		
		'''
		dataDF['EUI']=dataDF['EUIHeating']+dataDF['EUICooling']
		return dataDF

	def forHECSClf(self,dataDF):
		'''
		perprocessing the CBECS 2012 database for classifiction high performance buildings.
		'''
		self.getEUICooling(dataDF)
		self.getHECS(dataDF)
		return dataDF[dataDF['HECS']>=0.0]

	def getnumPeoplePerArea(self,dataDF):
		'''
		get the number of people per area
		'''
		numPeoplePerAreaSeries=dataDF['numEmployees']/dataDF['buildingArea']
		dataDF['numPeoplePerAreaCate']=pd.qcut(numPeoplePerAreaSeries,5,labels=[1,2,3,4,5]).astype('float64')
		return dataDF
		
	def forHEHSClf(self,dataDF):
		'''
		preprocessing the CBECS 2012 database for predicting whether a building is energy efficient in heating.
		'''
		dataDF=dataDF.fillna(0)
		#dataDF=dataDF[dataDF['climateZone']==1]
		dataDF['HDD65Category']=pd.cut(dataDF['HDD65'],5,labels=[1,2,3,4,5]).astype('float64')
		dataDF=dataDF.convert_objects(convert_numeric=True)
		dataDF=self.getnumPeoplePerArea(dataDF)
		dataDF=self.getEUIHeating(dataDF)
		dataDF=self.getHEHS(dataDF)
		return dataDF

	def forHEEBClf(self,dataDF):
		'''

		'''
		self.getEUI(dataDF)
		self.getHEES(dataDF)
		return dataDF[dataDF['HEEB']>=0.0]
		
	def forHECLClf(self,dataDF):
		'''
		for high performance cooling system classification

		'''
		dataDF=dataDF.fillna(0)
		self.getEUICooling(dataDF)
		dataDF=dataDF[dataDF['EUICooling']>0]
		dataDF=self.getHP(dataDF, energyType='EUICooling')
		return dataDF.dropna()
		 

class PreprocessingBEEMR(Preprocessing):
	'''
	Customized preprocess for BEEM.
	'''
	def __init__(self):
		#self.m,self.n = dataDF.shape
		#self.fillValue(dataDF)
		#self.checkKeywords(dataDF,Building)
		pass

	def replaceImproperdata(self, dataDF):
		'''
		
		'''
		try:
			dataDF.replace(-999, np.nan)
		except:
			pass

	def dataCleaningWithDecisionTree(self,BEEMRArray):

		'''
		Predict missing data using decision tree classifier.
		'''
		pass

	def fillValueWithImputer(self,dataDF):
		'''
		impute missing value by sklearn.preprocessing.Imputer
		'''
		imputer = Imputer()
		BEEMRArray=dataDF.values
		transformed_BEEMRArray = imputer.fit_transform(BEEMRArray)
		return transformed_BEEMRArray
		
	def fillValueWithMedian(self, dataDF):
		'''
		impute NaN value with median
		'''
		pass
class PreprocessingNYC(Preprocessing):
	'''
	
	'''
	def _init_(self):
		'''

		'''
		pass
		#dataDF=self.replaceStrwithNum(dataDF)

	def replaceStrwithNum(self,dataDF):
		'''
		
		'''
		name_list=list(range(1,28))
		name_list.append(np.nan)
		dataDF=dataDF.replace(['Office','Medical Office','College/University','Residence Hall/Dormitory','Hospital (General Medical & Surgical)',\
			'Mixed Use Property','Multifamily Housing','Worship Facility','Library','Social/Meeting Hall','Retail Store','Bank Branch','Financial Office',\
			'Enclosed Mall','K-12 School','Parking','Other - Recreation','Other - Specialty Hospital','Movie Theater','Manufacturing/Industrial Plant',\
			'Performing Arts','Senior Care Community','Supermarket/Grocery Store','Other - Entertainment/Public Assembly','Self-Storage Facility','Distribution Center',\
                'Other','Not Available'],name_list)
		dataDF=dataDF.replace(r'Whole',1,regex=True)
		dataDF=dataDF.fillna(0)
		return dataDF.convert_objects(convert_numeric=True)
	def forClf(self,dataDF):
		'''

		'''
		self.getHP(dataDF, energyType='SourceEUI')
		return dataDF



if __name__ == '__main__':

	pass
