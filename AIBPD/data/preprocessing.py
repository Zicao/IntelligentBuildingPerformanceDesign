'''
This class is used to pre-processing data for different goals, for example similarity analysis
'''
import numpy as np
import pandas as pd
from IntelligentBuildingPerformanceDesign.AIBPD.data.building import Building
class Preprocessing():
	m=0
	n=0
	def __init__(self,dataDF):
		self.m,self.n = dataDF.shape
		self.checkKeywords(dataDF,Building)
		self.fillValue(dataDF)

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


class PreprocessingCBECS(Preprocessing):

	def __init__(self,dataDF):
		self.m,self.n = dataDF.shape
		self.fillValue(dataDF)
		self.getEUICooling(dataDF)
		self.getHECS(dataDF)


	def getEUICooling(self,dataDF):
		'''
		calculate source energy usage intension for cooling. 
		Args:
			dataDF, the source data based on which the EUICooling is calculated.
		'''
		dataDF['EUICooling']=dataDF['ELCLBTU']*3.167+dataDF['NGCLBTU']*1.084\
								+dataDF['DHCLBTU']*3.613+dataDF['FKCLBTU']*1.05

	def getEUIHeating(self,dataDF):
		'''
		calculate source energy usage intension for heating. 
		Args:
			dataDF, the source data based on which the EUIHeating is calculated.
		'''
		dataDF['EUIHeating']=dataDF['ELHTBTU']*3.167+dataDF['NGHTBTU']*1.084\
								 +dataDF['DHHTBTU']*3.613+dataDF['FKHTBTU']*1.05
	def getHECS(self,dataDF):
		'''
		Buildings with the least EUICooling are sorted out. To increase credility, top 3% low 
		cooling energy buildings are abandoned. This low cooilng energy buildings are call High Efficient
		Cooling System (HECS).
		Args:
			dataDF, the source data based on which the EUIHeating is calculated.	
		'''
		top3=dataDF['EUICooling'].sort_values().iloc[int(0.03*self.m)]
		top23=dataDF['EUICooling'].sort_values().iloc[int(0.23*self.m)]
		hpcsList=[]
		for i in range(self.m):
			if dataDF['EUICooling'].loc[i]<=top23 and dataDF['EUICooling'].loc[i]>=top3:
				hpcsList.append(1)
			else:
				hpcsList.append(0)
		dataDF['HECS']=pd.Series(hpcsList)
		del hpcsList

class PreprocessingBEEMR(Preprocessing):
	'''
	Customized preprocess for BEEM.
	'''
	def __init__(self, dataDF):
		self.m,self.n = dataDF.shape
		self.fillValue(dataDF)
		self.checkKeywords(dataDF,Building)

	def replaceImproperdata(self, dataDF):
		'''
		
		'''
		try:
			dataDF.replace(-999, np.nan)
		except:
			pass

if __name__ == '__main__':
	frame = pd.DataFrame({'climateZone': range(7), 'b': range(7, 0, -1),\
	 'c': ['one', 'one', 'one', 'two', 'two', 'two', 'two'],'d': [0, 1, 2, 0, 1, 2, 3]})

	Preprocessing1=Preprocessing(frame)