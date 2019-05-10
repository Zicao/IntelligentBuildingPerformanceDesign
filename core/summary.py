import numpy as np


def standardReport(building,datasetDF,contents='all'):
	"""produce a standard reports.
	"""

	# rank based on source EUI
	n=np.searchsorted(self.datasetDF['EUI'].values,self.building)
	percentage_EUI=100*n/datasetDF.shape[0]
	print('The design building is in',percentage_EUI,'%, base on source EUI')

	#the position of end uses including heating, cooling, lighting, equipment and others.

	#the position of main features, such as external wall, windows.

def highlowReport(building,datasetDF,contents='all'):
	"""report competition between high and low performance building.
	"""
	pass


def dataset_summary_report(datasetDF,contents=None):
	"""produce a standard summary report for the dataset.
	Parameters:
	----------
	
	Return:
	----------
	"""
	#EUI distribution.
	datasetDF['EUI'].hist()
	




__all__=['standardReport','highlowReport']