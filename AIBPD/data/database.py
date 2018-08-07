'''
# Copyright (c) 2013-2018, Zhichao Tian <tzchao123@qq.com> 
'''
import pandas as pd
import re
import os
from IntelligentBuildingPerformanceDesign.AIBPD.data.preprocessing import PreprocessingCBECS, PreprocessingBEEMR

class Database():
	"""docstring for Database"""
	databaseList=['CBECS2012','BEEMR']
	databasePath='H:\Codes\IntelligentBuildingPerformanceDesign\\resources\\'
	def __init__(self):
		super(Database, self).__init__()

	def select(self,databaseName):
		'''
		match the databaseName with the embedded database. 
		If it exist, return the true name, otherwise a error message.
		Args:
			databaseName, database name
		'''
		if re.search(databaseName,'CBECS2012'):
			print("Load successfully")
			return self.loadDatabaseCBECS(self.databasePath+'CBECS2012.csv')
		elif re.search(databaseName,'BEEMR'):
			print("Load successfully")
			self.databasePath=self.databasePath+'BEEMR.csv'
			return self.loadDatabaseBEEM(self.databasePath+'BEEMR.csv')
		else:
			print("Error with find datbase.\n","Available databases include", self.databaseList)

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
		preprocessDF=PreprocessingCBECS(dataDF)
		return dataDF

	def loadDatabaseBEEM(self,databaseName):
		'''
		Load database using pandas DataFrame object.
		Args:
			databaseName, the name of the database.
		Return:
			dataDF, pandas DataFrame object
		'''
		dataDF=pd.read_csv(databaseName,header=0,encoding='utf8')
		preprocessDF=PreprocessingBEEMR(dataDF)
		return dataDF

	def existDatabaseList(self):
		print("Available databases include",self.databaseList)

	def addData2DB(self,oneBuilding):
		'''
		Add a new building data into the database.
		Args:
			oneBuilding, a Building object.
		'''
		


		
if __name__ == '__main__':
	database=Database()
	CBECS2012DF=database.select('CBECS2012')
	print(type(CBECS2012DF))




		