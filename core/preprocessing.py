"""pre-processing the database
"""
from tkinter import filedialog
from tkinter import Tk
import pandas as pd
import numpy as np

def loadMetadata(self,fileName=None):
	"""load the metadata of the database which contains the description 
	of the databse.
	"""
	
	if not fileName:
		Tk().withdraw()
		filePath=filedialog.askopenfilename()
		#check whether it is a csv file.
		if re.search('\.csv',filePath):
			self._datasetDF=self.loadDatabaseCBECS(filePath)
			print('Dataset in',filePath,'has been loaded!')
		else:
			print('Please select a valid file. Accepted file format: csv')
		return self._datasetDF
	else:
		self.select_with_name(databaseName=fileName)
def 