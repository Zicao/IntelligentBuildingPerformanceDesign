'''
# Copyright (c) 2013-2018, Zhichao Tian <tzchao123@qq.com> 
'''
import pandas as pd
import numpy as np
import csv
import re
import os
from aibpd.data.preprocessing import PreprocessingCBECS, PreprocessingBEEMR, PreprocessingNYC
from aibpd.__init__ import currentUrl
from tkinter import filedialog
from tkinter import Tk


class Database():
	"""docstring for Database"""
	databaseList=['CBECS2012','BEEMR']
	databasePath=currentUrl+'\\resources\\'
	_datasetDF=None
	#datasetDF=None
	metadataDF=None

	def __init__(self):
		super(Database, self).__init__()
		if not self._datasetDF:
			print('Please select a database to continue the analysis')
	@property
	def datasetDF(self):
		return self._datasetDF

	@datasetDF.setter
	def datasetDF(self,value):
		self._datasetDF=value

	
	def select_with_name(self,databaseName=None,metadata=False):
		'''
		match the databaseName with the embedded database. 
		If it exist, return the true name, otherwise a error message.
		Parameters:
			databaseName, database name
		'''
		if re.search(databaseName,'CBECS2012'):
			print("Load CBECS2012 successfully")
			self._datasetDF=self.loadDatabaseCBECS(self.databasePath+'CBECS2012.csv')
			if metadata:
				self.metadataDF = pd.read_csv(self.databasePath+'CBECS2012_metadata.csv')
		elif re.search(databaseName,'BEEMR'):
			print("Load BEEMR successfully")
			self._datasetDF=self.loadBEEM2DF(self.databasePath+'BEEMR.csv')
		elif re.search(databaseName,'nyc_benchmarking_disclosure_data_reported_in_2017'):
			self._datasetDF=self.loadNYC2DF(self.databasePath+'nyc_benchmarking_disclosure_data_reported_in_2017.csv')
		else:
			print("Error with find datbase.\n","Available databases include", self.databaseList)
		
		if not metadata:
			return self._datasetDF
		else:
			return self._datasetDF,self.metadataDF

	def select(self):
		"""select a database with a dialog

		Return:
		----------
		datasetDF, a DataFrame object.

		Example:
		----------
		After processing the datasetDF, you can also feedback this datasetDF 
			to the Database object using this code:
			db1.datasetDF=datasetDF
		"""
		Tk().withdraw()
		filePath=filedialog.askopenfilename()
		#check whether it is a csv file.
		if re.search('\.csv',filePath):
			self._datasetDF=self.loadDatabaseCBECS(filePath)
		else:
			print('Please select a valid file. Accepted file format: csv')
		return self._datasetDF

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
			dataDF=pd.read_csv(databaseName,header=0)
		except Exception as e:
			raise e
		dataDF=dataDF.fillna(0)
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
		"""save the datasetDF into a new database in various format (default csv)

		Parameters:
		----------
		name, the name of the database.
		format, the format of the database.

		Return:
		----------
		"""
		filePath=filedialog.askdirectory()
		filePath+='/'
		filePath+=name
		filePath+='.csv'
		if not self._datasetDF.empty:
			self._datasetDF.to_csv(path_or_buf=filePath)
			print('datasetDF has been saved to',filePath)
		else:
			print('The datasetDF is empty!')
		


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
		dataDF, a dataframe object that contains the dataset
		"""
		#get the EUI feature.
		if dataDF:
			self._datasetDF=dataDF
		self.getEUI(self._datasetDF)
		return self._datasetDF

		
if __name__ == '__main__':
	database=Database()
	CBECS_DF=database.select('CBECS2012')
	Preproc=PreprocessingCBECS()
	CBECS_DF=CBECS_DF[CBECS_DF['HDD65']>=3000]

	CBECS_DF=Preproc.forHEHSClf(CBECS_DF)
	HP=CBECS_DF[CBECS_DF['HEHS']==1.0]
	MP=CBECS_DF[CBECS_DF['HEHS']==2.0]
	LP=CBECS_DF[CBECS_DF['HEHS']==3.0]
	print(HP['EUIHeating'].mean(),HP['EUIHeating'].std())
	print(MP['EUIHeating'].mean(),MP['EUIHeating'].std())
	print(LP['EUIHeating'].mean(),LP['EUIHeating'].std())
