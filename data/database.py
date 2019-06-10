'''
# Copyright (c) 2013-2018, Zhichao Tian <tzchao123@qq.com> 
'''
import pandas as pd
import numpy as np
import csv
import re
import os
from aibpd.__init__ import currentUrl
from tkinter import filedialog
from tkinter import Tk
from aibpd.core.summary import raw_summary


class Database():
	"""docstring for Database"""
	databaseList=['CBECS2012','BEEMR']
	databasePath=currentUrl+'\\resources\\'
	_dataDF=pd.DataFrame()

	#a metadataDF contains the various description of the variables.
	#categoricalFeaturelist
	main_features=['buildingAreaCategory','buildingShape','censusRegion',
				'climateZone','HDD65','HVACUpgrade','insulationUpgrade',
				'MAINCL','MAINHT','numEmployeesCategory','numFloors',
				'OWNTYPE', 'region','RENWLL','lightingUpgrade',
				'roofConstruction','STUSED','OPEN24','wallConstruction' ,
				'WINTYP','WKHRSC','WWR','yrConstructionCategory']
	main_features_simpleimpute=['HVACUpgrade','insulationUpgrade','RENWLL',
				'lightingUpgrade']
	main_features_remove=['MAINCL','MAINHT']

	main_feature_categorical=['buildingAreaCategory', 'buildingShape', 'censusRegion',
				 'climateZone', 'HVACUpgrade', 'insulationUpgrade', 'MAINCL', 'MAINHT', 
				 'numEmployeesCategory', 'openWeekend', 'OWNTYPE', 
				 'region', 'RENWLL', 'lightingUpgrade', 'roofConstruction', 
				 'STUSED', 'OPEN24', 'wallConstruction', 'WINTYP', 
				 'WKHRSC', 'roofTilt', 'windowTilt', 'EQGLSS', 'reflectiveWindow', 
				 'skylights', 'windowUpgrade', 'OWNOCC', 'energyPlan', 'oneActivity', 
				 'FACIL', 'FKUSED', 'PRUSED', 'NGHT1', 'CLVCAV', 'CLVVAV', 'EMCS', 
				 'HWRDHT', 'HWRDCL', 'ECN', 'ELWATR', 'FLUOR', 'CFLR', 'BULB', 
				 'HALO', 'HID', 'LED', 'SCHED', 'OCSN', 'NOCC','LTOHRP', 'LTNHRP',
				 'DAYLTP','principleActivity','yrConstructionCategory']

	main_feature_numeric=['buildingArea','HDD65', 'HEATP', 'MONUSE', 'numFloors', 'WWR','yearOfConstruction']
	'''
	main_featuresCBECS_Categorical1=['CENDIV','WLCNS','RFCNS','RFCOOL','RFTILT',
				'WINTYP','TINT','GLSSPC','EQGLSS','REFL','SKYLT','ATTIC',
				'AWN','BLDSHP','RENWIN','RENRFF','RENWLL','RENHVC','RENELC',
				'RENINS','OPEN24','OPENWE','OWNTYPE','OWNOCC','OWNOPR','ENRGYPLN',
				'ONEACT','FACIL','FKUSED','PRUSED','STUSED','ELHT1','NGHT1','MAINHT',
				'HTVCAV','HTVVAV','ELCOOL','NGCOOL','MAINCL','CLVCAV','CLVVAV',
				'EMCS','HWRDHT','HWRDCL','ECN','MAINT','ELWATR','FLUOR','CFLR',
				'BULB','HALO','HID','LED','SCHED','OCSN','RENLGT']
	main_featuresCBECS_numeric1=['SQFT','NFLOOR','FLCEILHT','YRCON','NOCC','OCCUPYP',
				'WKHRS','WKER','HEATP','COOLP','HDD65','CDD65','NPCTERM','NPCTERM',
				'NLAPTP','NPRNTR','NCOPIER','LTOHRP','LTNHRP','DAYLTP']
	main_featuresCBECS_Categorical=['buildingAreaCategory', 'buildingShape', 'censusRegion',
				 'climateZone', 'HVACUpgrade', 'insulationUpgrade', 'MAINCL', 'MAINHT', 
				 'numEmployeesCategory', 'openWeekend', 'OWNTYPE', 
				 'region', 'RENWLL', 'lightingUpgrade', 'roofConstruction', 
				 'STUSED', 'OPEN24', 'wallConstruction', 'WHOPPR', 'WINTYP', 
				 'WKHRSC', 'roofTilt', 'windowTilt', 'EQGLSS', 'reflectiveWindow', 
				 'skylights', 'windowUpgrade', 'OWNOCC', 'energyPlan', 'oneActivity', 
				 'FACIL', 'FKUSED', 'PRUSED', 'NGHT1', 'CLVCAV', 'CLVVAV', 'EMCS', 
				 'HWRDHT', 'HWRDCL', 'ECN', 'ELWATR', 'FLUOR', 'CFLR', 'BULB', 
				 'HALO', 'HID', 'LED', 'SCHED', 'OCSN', 'NOCC','LTOHRP', 'LTNHRP', 'DAYLTP']
	main_featuresCBECS_numeric=['HDD65', 'HEATP', 'MONUSE', 'numFloors', 'WWR',
				'yearOfConstruction']
	'''
	
	_matedataDF=None
	def __init__(self,file_path=None, dataDF=pd.DataFrame()):
		super(Database, self).__init__()
		if self._dataDF.empty:
			print('Please select a database to continue the analysis')
		if file_path:
			self._dataDF=self.select(file_path)
		if not dataDF.empty:
			self._dataDF=dataDF
		if not self._dataDF.empty:
			raw_summary(self._dataDF,feature_list=self.main_features)

	@property
	def dataDF(self):
		return self._dataDF

	@dataDF.setter
	def dataDF(self,value):
		self._dataDF=value

	@property
	def metadataDF(self):
		return self._matedataDF
	@metadataDF.setter
	def metadataDF(self,value):
		self._matedataDF=value
	

	
	def select_with_name(self,databaseName=None,metadata=False):
		'''
		match the databaseName with the embedded database. 
		If it exist, return the true name, otherwise a error message.
		Parameters:
			databaseName, database name
		'''
		file_pathList=os.listdir(self.databasePath)
		for file_path in file_pathList:
			if re.search(databaseName,file_path):
				self._dataDF=self.loadDatabaseCBECS(self.databasePath+file_path)
				print(file_path,'has been loaded.')
		if not metadata:
			return self._dataDF
		else:
			return self._dataDF,self.metadataDF

	def select(self, fileName=None, metadata=None):
		"""select a database with a dialog
		
		Parameters:
		----------
		fileName, a file that contains the data.
		metadata, whether to select a metadata file.
		Return:
		----------

		Example:
		----------
		After processing the dataDF, you can also feedback this dataDF 
			to the Database object using this code:
			db1.dataDF=dataDF
		"""
		if not fileName:
			Tk().withdraw()
			file_path=filedialog.askopenfilename()
			#check whether it is a csv file.
			if re.search('\.csv',file_path):
				self._dataDF=self.loadDatabaseCBECS(file_path)
				print('Dataset in',file_path,'has been loaded!')
			else:
				print('Please select a valid file. Accepted file format: csv')
		else:
			self.select_with_name(databaseName=fileName)

		if metadata:
			Tk().withdraw()
			metaFilePath=filedialog.askopenfilename()
			if re.search('\.csv'.metaFilePath):
				self._matedataDF = pd.read_csv(metaFilePath)
				print('The metadata file have been loaded in', metaFilePath)
			else:
				print('Please select a valid file.')
		return self._dataDF




	def loadNYC2DF(self,path):
		'''

		'''
		dataDF=pd.read_csv(path,header=0)
		preprocessDF=PreprocessingNYC(dataDF)
		return dataDF

	def addNewDatabase(self,databaseName):
		absolutePath=databasePath+databaseName
		if os.path.exists(absolutePath):
			print("databaseName have already existed in your computer")
		else:
			os.chdir(databasePath)
			self.databaseList.append(databaseName)


	def loadDatabaseCBECS(self,databaseName):
		'''
		Load database using pandas DataFrame object.
		Parameters:
		-------------
			databaseName, the name of the database.
		
		Return:
		------------
			dataDF, a DataFrame object that contain the data.
		'''
		dataDF=None
		try:
			dataDF=pd.read_csv(databaseName,header=0,encoding = "ISO-8859-1")
		except Exception as e:
			print(e)	
		
		return dataDF

	def loadBEEMR2DF(self):
		'''
		Load database using pandas DataFrame object.
		Args:
			databaseName, the name of the database.
		Return:
			dataDF, pandas DataFrame object
		'''
		databaseName=self.databasePath+'BEEMR.csv'
		BEEMRDF=pd.read_csv(databaseName,header=0,encoding='utf8')
		preprocessDF=PreprocessingBEEMR(BEEMRDF)
		return preprocessDF

	def loadBEEMR2Array(self):
		'''
		load database and save it into numpy array file
		'''
		databaseName=self.databasePath+'BEEMR.csv'
		BEEMRDF=self.loadBEEMR2DF()
		return BEEMRDF.values

	def existDatabaseList(self):
		print("Available databases include",self.databaseList)


	def addData2DB(self,oneBuilding):
		'''
		Add a new building data into the database.
		Args:
			oneBuilding, a Building object.
		'''
		pass

	def checkDatabase(self, dataDF):
		'''
		check the database. 1) whether each columns contain abnormal data.
							2)
		'''
		pass
	def save(self,name='MyDatabase', format='csv'):
		"""save the dataDF into a new database in various format (default csv)

		Parameters:
		----------
		name, the name of the database.
		format, the format of the database.

		Return:
		----------
		"""
		file_path=filedialog.askdirectory()
		file_path+='/'
		file_path+=name
		file_path+='.csv'
		if not self._dataDF.empty:
			self._dataDF.to_csv(path_or_buf=file_path)
			print('dataDF has been saved to',file_path)
		else:
			print('The dataDF is empty!')
		


	def summaryDataset(self):
		'''
		summary the the basic situation of a database using the Summary class.
		Args:

		'''
		pass

	def prep4EUIReg(self,dataDF=None):
		"""proprocess dataDF for EUI regression
		Parameters:
		----------
		Return:
		----------
		dataDF, a dataframe object that contains the data
		"""
		#get the EUI feature.
		if dataDF:
			self._dataDF=dataDF
		self.getEUI(self._dataDF)
		return self._dataDF
	def find_building_by_ID(self,ID=None):
		"""find a building in a database
		Parameter
		----------
		ID, the ID of the building.
		Return
		----------
		building, a Building Object.
		"""
		buildings=self.dataDF[self.dataDF['ID']>=ID][self.dataDF['ID']<=ID]
		if buildings.shape[0]>1:
			print('Multi-buildings are found. The first one is returned')
		building_series=buildings.iloc[buildings.index[0]]
		return building_series

		
if __name__ == '__main__':
	database=Database()
	CBECS_DF=database.select('CBECS2012.csv')
