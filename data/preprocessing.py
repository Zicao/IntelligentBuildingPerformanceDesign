
import numpy as np
import pandas as pd
from tkinter import filedialog
from tkinter import Tk
from aibpd.data.building import Building
from sklearn.preprocessing import Imputer
from aibpd.data.weather import Weather
from aibpd.data.database import Database
from sklearn.preprocessing import MinMaxScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
#from sklearn.impute import IterativeImputer

class Preprocessing():
	'''
	This class is used to pre-processing data for different goals, for example similarity analysis
	'''
	def __init__(self):
		#self.m,self.n = dataDF.shape
		#self.checkKeywords(dataDF,Building)
		#self.fillValue(dataDF)
		pass

	def general(self,dataDF):
		'''
		general preprocesses such as fill NaN with 0
		'''
		dataDF.fillna(0)

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
						0= 'EUI', => 'HPLV' marks the level of heating performance, 1 for high performance, 2 for medium, 
							0 for low level, and 3 for others.
						1='HEUI' => 'HEHS'= high efficient heating system
						2='CEUI' => 'HPLV' = high efficient cooling system
						3='designHeatingLoad' => 'HEE4H' = high efficient envelop system for heating.
						4='designCoolingLoad' => 'HEE4C' = high efficient envelop system for cooling.
		'''
		
		try:
			#energyTypeDict={0:'EUI',1:'HEUI',2:'CEUI',3:'designHeatingLoad',4:'designCoolingLoad'}
			highEfficientType={'EUI': 'PLV','HEUI': 'HPLV','CEUI': 'CPLV','designHeatingLoad':'HEE4H',
								'designCoolingLoad':'HEE4C',
								'WNEUI':'WNLV','TNEUI':'WNLV','TNLV':'TNLV'}
			isHEName=highEfficientType[energyType]
			
		except:
			energyName='EUI'
			isHEName='HPLV'
		#dataDF=dataDF[dataDF[energyType]>0]
		print('dataDF in preprocessing shape',dataDF.shape,'level',isHEName)
		top3=dataDF[energyType].sort_values().iloc[int(0.03*dataDF.shape[0])]
		top23=dataDF[energyType].sort_values().iloc[int(0.23*dataDF.shape[0])]
		top10=dataDF[energyType].sort_values().iloc[int(0.10*dataDF.shape[0])]
		top25=dataDF[energyType].sort_values().iloc[int(0.25*dataDF.shape[0])]
		top75=dataDF[energyType].sort_values().iloc[int(0.75*dataDF.shape[0])]
		top90=dataDF[energyType].sort_values().iloc[int(0.90*dataDF.shape[0])]
		hpcsList=[]
		hpcsList_index=[]
		print('top3',top3,'top10',top10,'top23',top23,'top25',top25,'top75',top75,'top90',top90)
		for index,row in dataDF.iterrows():
			if row[energyType]<=top25 and row[energyType]>top10:
				hpcsList.append(1.0)
			elif row[energyType]<=top75 and row[energyType]>top25:
				hpcsList.append(2.0)
			elif row[energyType]<=top90 and row[energyType]>top75:
				hpcsList.append(0.0)
			else:
				hpcsList.append(3.0)
			hpcsList_index.append(index)
		dataSeries=pd.Series(hpcsList,index=hpcsList_index)
		#dataDF1=dataDF.add(dataDF2, fill_value=0)
		dataDF[isHEName]=dataSeries
		del hpcsList
		return dataDF


	def addweatherData(self,dataDF):
		'''
		add weather data in to dataDF by city name.
		'''
		Weather.addWeatherAttributesIntoDataDFByCity(dataDF)

class PreprocessingCBECS(Preprocessing):
	"""Preprocessing the CBECS data
	"""
	
	
	def __init__(self, data=None):
		if isinstance(data, Database):
			dataDF = data._dataDF
		elif isinstance(data, pd.DataFrame):
			dataDF = data
		else:
			dataDF = data._dataDF
		self.get_EUI(dataDF)
		self.get_HEUI(dataDF)
		self.get_CEUI(dataDF)
		self.get_WNEUI(dataDF)
		self.get_TNEUI(dataDF)

		self.get_HPLV(dataDF) #get the heating performance level.
		self.get_CPLV(dataDF) #get the cooling performance level.
		self.get_PLV(dataDF) # get the EUI performance level for classification
		self.get_TNLV(dataDF) #get 
		self.get_WNLV(dataDF) #get
		X_feature_list_MAINHT=['buildingAreaCategory','censusRegion','OWNTYPE','WKHRSC','WWR']
		X_feature_list_MAINCL=['buildingAreaCategory','roofConstruction','OWNTYPE','WKHRSC','WWR']
		self.impute_svm(dataDF,feature_list=['MAINHT'],X_feature_list=X_feature_list_MAINHT)
		self.impute_svm(dataDF,feature_list=['MAINCL'],X_feature_list=X_feature_list_MAINCL)
		self.impute_with_constant(dataDF,feature_list=Database.feature_impute_constant) #impute
		dataDF.fillna(0)
		
		if isinstance(data, Database):
			data.dataDF = dataDF
		elif isinstance(data, pd.DataFrame):
			data =dataDF
		else:
			data.dataDF = dataDF
		



	def numeric_transform(self, dataDF=None, feature_list=None):
		"""
		"""
		if 'yearOfConstruction' in feature_list:
			data=dataDF['yearOfConstruction'].replace(995,1964)
			dataDF['yearOfConstruction']=(data-1964)/66
		return dataDF

	def minmax_transform(self,dataDF=None,feature_list=None):
		"""transform the data.
		"""
		for feature in feature_list:
			scaler = MinMaxScaler()
			scaler.fit(dataDF[feature].values.reshape(1,-1))
			data=scaler.fit_transform(dataDF[feature].values.reshape(1,-1))
			dataDF[feature] = pd.Series(data[0])
		return dataDF


	def impute_with_constant(self,dataDF=None,feature_list=None,value=0):
		"""impute with zero
		"""
		for feature in feature_list:
			data=dataDF[feature].fillna(value)
			dataDF[feature]=data
		return dataDF

	def IterativeImputer_decisiontree(self, dataDF=None, feature_list=None, X_feature_list= None, **kwds):
		"""impute the missing data with sklearn iterative imputer
		parameters:
		----------
		dataDF,
		feature_list,
		X_feature_list,

		Return:
		----------
		dataDF:

		"""
		for feature in feature_list:
			fullDF=dataDF[dataDF[feature]<1000]
			X_full=fullDF[X_feature_list]
			y_full=fullDF[feature]
			X_missing=dataDF[dataDF[feature]>1000][X_feature_list]
			dt_clf = DecisionTreeClassifier(random_state=0)
			#imp=IterativeImputer(random_state=0, estimator=dt_clf)
			dt_clf.fit(X_full.values,y_full.values)
			Y_missing=dt_clf.predict(X_missing.values)
		return dataDF

	def impute_svm(self, dataDF=None,feature_list=None, X_feature_list= None, **kwds):
		"""
		"""
		for feature in feature_list:
			data=dataDF[feature].isnull()
			missing_index=data[data==True].index
			full_index=data[data==False].index
			X_full=dataDF.iloc[full_index][X_feature_list].fillna(0)
			y_full=dataDF.iloc[full_index][feature]
			X_missing=dataDF.iloc[missing_index][X_feature_list].fillna(0)
			svm_clf = SVC(gamma='auto')
			svm_clf.fit(X_full.values,y_full.values)
			y_pred=svm_clf.predict(X_missing.values)
			for i in range(missing_index.shape[0]):
				dataDF[feature][missing_index[i]]=y_pred[i]
		return dataDF


		
	def get_CEUI(self,dataDF):
		'''
		calculate source energy usage intension for cooling. 
		Args:
			dataDF, the source data based on which the CEUI is calculated.
		'''
		#dataDF['CEUI']=(dataDF['ELCLBTU']*3.167+dataDF['NGCLBTU']*1.084\
								#+dataDF['DHCLBTU']*3.613+dataDF['FKCLBTU']*1.05)/dataDF['buildingArea']

		if not 'CEUI' in dataDF.columns:
			dataDF['CEUI']=dataDF['MFCLBTU']/dataDF['buildingArea']
		return dataDF


	def get_HEUI(self,dataDF):
		'''
		calculate sources energy usage intension for heating
		'''
		if not 'HEUI' in dataDF.columns:
			dataDF['HEUI']=dataDF['MFHTBTU']/dataDF['buildingArea']
		return dataDF

	def get_EUI(self,dataDF):
		'''calculate the EUI of the buildings.
		
		'''
		if not 'EUI' in dataDF.columns:
			dataDF['EUI']=(dataDF['MFHTBTU']+dataDF['MFCLBTU']+dataDF['MFVNBTU']+\
				dataDF['MFWTBTU']+dataDF['MFLTBTU']+dataDF['MFCKBTU']+\
				dataDF['MFOFBTU']+dataDF['MFPCBTU']+dataDF['MFOTBTU'])/dataDF['buildingArea']
		return dataDF

	def get_WNEUI(self,dataDF):
		"""get the weather normalized EUI.
		Parameters:
		----------
		dataDF, the DataFrame object that contains the data.

		Return:
		----------
		dataDF, same as previous.
		"""
		try:
			dataDF['WNEUI']=dataDF['EUI']/(dataDF['CDD65']+dataDF['HDD65'])
		except ZeroDivisionError:
			print('Cannot calculate the WNEUI, please check the CDD65 and HDD65')
		return dataDF

	def get_TNEUI(self,dataDF,method='week'):
		"""get the time normalized EUI
		Parameters:
		----------
		dataDF, a DataFrame object that contains the data.
		method, set the method to define the normalized time.

		Return:
		----------
		dataDF, a DataFrame object that contains the data.
		"""
		if 'WKHRS' in dataDF.columns:
			dataDF['TNEUI']=dataDF['EUI']/dataDF['WKHRS']
		else:
			print('WKHRS (open hours per week) is not a feature of this data')
		return dataDF

	def get_PLV(self,dataDF):
		'''

		'''
		self.getHP(dataDF, energyType='EUI')

	def get_CPLV(self,dataDF):
		'''
		Buildings with the least CEUI are sorted out. To increase credility, top 3% low 
		cooling energy buildings are abandoned. This low cooilng energy buildings are call High Efficient
		Cooling System (coolingLevel).
		Args:
			dataDF, the source data based on which the HEUI is calculated.	
		'''
		self.getHP(dataDF, energyType='CEUI')


	def get_HPLV(self,dataDF):
		"""
		
		"""
		if not 'HPLV' in dataDF.columns:
			print('HPLV exists, if you want to generate a new HPLV\
				please delete exists ones')
			return self.getHP(dataDF, energyType='HEUI')
		else:
			return dataDF

	def get_WNLV(self,dataDF):
		"""
		"""
		pass

	def get_TNLV(self,dataDF):
		"""
		"""
		pass

	def for_HPLV_clf(self,dataDF):
		'''
		Perprocessing the CBECS 2012 database for heating performance classification.
		'''
		self.general(dataDF)
		self.get_HEUI(dataDF)
		self.get_HPLV(dataDF)
		return dataDF[dataDF['HPLV']>=0.0]

	def for_CPLV_clf(self,dataDF):
		'''
		Perprocessing the CBECS 2012 database for cooling performance classification.
		'''
		self.general(dataDF)
		self.get_CEUI(dataDF)
		self.get_CPLV(dataDF)
		return dataDF

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
		dataDF=self.get_HEUI(dataDF)
		dataDF=self.getHEHS(dataDF)
		return dataDF

		
	def forHECLClf(self,dataDF):
		'''
		for high performance cooling system classification

		'''
		dataDF=dataDF.fillna(0)
		self.get_CEUI(dataDF)
		dataDF=dataDF[dataDF['CEUI']>0]
		dataDF=self.getHP(dataDF, energyType='CEUI')
		return dataDF.dropna()

	def prep4EUIReg(self,dataDF):
		"""proprocess dataDF for EUI regression
		Parameters:
		----------
		Return:
		----------
		dataDF, a dataframe object that contains the data
		"""
		#get the EUI feature.
		dataDF=self.get_EUI(dataDF)
		return dataDF
	
		 

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
