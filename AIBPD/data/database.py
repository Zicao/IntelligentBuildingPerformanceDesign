'''
# Copyright (c) 2013-2018, Zhichao Tian <tzchao123@qq.com> 
'''
import pandas as pd
import re
import os
from IntelligentBuildingPerformanceDesign.AIBPD.data.preprocessing import PreprocessingCBECS

class Database():
	"""docstring for Database"""
	databaseList=['CBECS2012']
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
		for i in self.databaseList:
			if re.search(databaseName,i):
				print("Load sucessfully")
				return self.loadDatabaseCBECS(self.databasePath+i+'.csv')
		print("Error with find datbase.\n","Available databases include", self.databaseList)

	def addNewDatabase(self,databaseName):
		absolutePath=databasePath+databaseName
		if os.path.exists(absolutePath):
			print("databaseName have already existed in your computer")
		else:
			os.chdir(databasePath)
			self.databaseList.append(databaseName)


	def loadDatabaseCBECS(self,databaseName):
		dataDataFrame=pd.DataFrame(pd.read_csv(databaseName,header=0))
		preprocessDF=PreprocessingCBECS(dataDataFrame)
		return dataDataFrame

	def existDatabaseList(self):
		print("Available databases include",self.databaseList)

		
if __name__ == '__main__':
	database=Database()
	CBECS2012DF=database.select('CBECS2012')
	print(type(CBECS2012DF))




		