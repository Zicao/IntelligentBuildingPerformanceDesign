'''
# Copyright (c) 2013-2018, Zhichao Tian <tzchao123@qq.com> 
'''
import pandas as pd
import numpy as np
import csv
import re
import os
from IntelligentBuildingPerformanceDesign.AIBPD.data.preprocessing import PreprocessingCBECS, PreprocessingBEEMR, PreprocessingNYC
from IntelligentBuildingPerformanceDesign.__init__ import currentUrl
class Database():
	"""docstring for Database"""
	databaseList=['CBECS2012','BEEMR']
	databasePath=currentUrl+'\\resources\\'
	def __init__(self):
		super(Database, self).__init__()
		#self.select(databaseName)

	def select(self,databaseName):
		'''
		match the databaseName with the embedded database. 
		If it exist, return the true name, otherwise a error message.
		Args:
			databaseName, database name
		'''
		if re.search(databaseName,'CBECS2012'):
			print("Load CBECS2012 successfully")
			return self.loadDatabaseCBECS(self.databasePath+'CBECS2012.csv')
		elif re.search(databaseName,'BEEMR'):
			print("Load BEEMR successfully")
			return self.loadBEEM2DF(self.databasePath+'BEEMR.csv')
		elif re.search(databaseName,'nyc_benchmarking_disclosure_data_reported_in_2017'):
			return self.loadNYC2DF(self.databasePath+'nyc_benchmarking_disclosure_data_reported_in_2017.csv')
		else:
			print("Error with find datbase.\n","Available databases include", self.databaseList)
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
		Args:
			databaseName, the name of the database.
		'''
		dataDF=pd.read_csv(databaseName,header=0)
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


		
if __name__ == '__main__':
	database=Database()
	CBECS_DF=database.select('CBECS2012')
	Preproc=PreprocessingCBECS()
	CBECS_DF=Preproc.forHEHSClf(CBECS_DF)
	print(CBECS_DF)
	HP=CBECS_DF[CBECS_DF['HEHS']==1.0]
	MP=CBECS_DF[CBECS_DF['HEHS']==2.0]
	LP=CBECS_DF[CBECS_DF['HEHS']==3.0]
	print(HP['EUIHeating'].mean(),HP['EUIHeating'].std())
	print(MP['EUIHeating'].mean(),MP['EUIHeating'].std())
	print(LP['EUIHeating'].mean(),LP['EUIHeating'].std())
	HP[['HDD65Category']].hist(bins=100,density=False)
	MP[['HDD65Category']].hist(bins=100,density=False)
	LP[['HDD65Category']].hist(bins=100,density=False)