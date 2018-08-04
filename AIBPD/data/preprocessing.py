'''
This class is used to pre-processing data for different goals, for example similarity analysis
'''
import numpy as np
import pandas as pd
class Preprocessing():

	def __init__(self,dataDF):
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


if __name__ == '__main__':
	pass