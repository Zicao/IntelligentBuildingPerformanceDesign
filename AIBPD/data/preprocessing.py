'''
This class is used to pre-processing data for different goals, for example similarity analysis
'''
import numpy as np
import pandas as pd
class Preprocessing():
	
	def __init__(self,dataDF):
		self.dataDF=dataDF

	def cleaning(self):
		
		pass;
	def mapping(self):
		
		pass;
	def fillValue(self):
		'''
		fill none with Value 0
		Return:
			post processed dataDF object
		'''
		self.dataDF.fillna(value=0)

class PreprocessingCBECS(Preprocessing):

	def __init__(self,dataDF):
		self.dataDF=dataDF
		self.m,self.n = dataDF.shape

	def getEUICooling(self):
		self.dataDF['EUICooling']=self.dataDF['ELCLBTU']*3.167+self.dataDF['NGCLBTU']*1.084\
								+self.dataDF['DHCLBTU']*3.613+self.dataDF['FKCLBTU']*1.05

	def getEUIHeating(self):
		self.dataDF['EUIHeating']=self.dataDF['ELHTBTU']*3.167+self.dataDF['NGHTBTU']*1.084\
								 +self.dataDF['DHHTBTU']*3.613+self.dataDF['FKHTBTU']*1.05
	def getHECS(self):
		top3=self.dataDF['EUICooling'].sort_values().iloc[int(0.03*self.m)]
		top23=self.dataDF['EUICooling'].sort_values().iloc[int(0.23*self.m)]
		hpcsList=[]
		for i in range(m):
			if self.dataDF['EUICooling'].loc[i]<=top23 and self.dataDF['EUICooling'].loc[i]>=top3:
				hpcsList.append(1)
			else:
				hpcsList.append(0)
		self.dataDF['HECS']=pd.Series(hpcsList)
		del hpcsList


if __name__ == '__main__':
	pass