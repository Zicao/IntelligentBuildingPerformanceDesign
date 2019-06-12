#Quantify the potential of different measures.
import pandas as pd
def potential(database=None,building=None,
	target='EUI',
	algorithm='DecisionTree'):
	"""Quantify the energy improvement potiential of different measures.
	"""
	pass

def potiential_svm(database=None,building=None,target='EUI',**kwds):
	"""Quantify the enregy improvement potiential of different measures with SVM.
	Parameters:
	----------
	database, a Database object that contains the data.
	building, a Building object represents the target building.
	target, the objective.
	**kwds, all other key words to be passed to "sklearn svm svc"
	"""
	pass
