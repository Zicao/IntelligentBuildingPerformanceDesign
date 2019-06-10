import numpy as np
import matplotlib.pyplot as plt
#import aibpd.data.database as db
import pandas as pd
__all__=['raw_summary','summary','standard_report','highlowReport','dataset_summary']

def raw_summary(dataDF,feature_list=None):
	"""summarize the dataDF before it has been preprocessing
	"""
	missing_status=missing_values_table(dataDF,feature_list)
	print(missing_status)
	return missing_status

def summary(database, building=pd.Series()):
	"""summary the dataDF or the building
	"""
	dataDF=database.dataDF
	if building.empty:
		dataset_summary(dataDF)
	else:
		standard_report(dataDF,building)
		

def dataset_summary(dataDF,contents=None):
	"""produce a standard summary report for the dataset.
	Parameters:
	----------
	
	Return:
	----------
	"""
	#shows the EUI, weather nomalized EUI, heating EUI, Cooling EUI distribution.
	#dataDF['EUI'].hist()
	#summarize the percentages of missing value of each columns
	mis_val_table_ren_columns=missing_values_table(dataDF)
	print(mis_val_table_ren_columns)

	#shows the EUI distribution
	EUI_list=['EUI','HEUI','CEUI','WNEUI','TNEUI']
	dataDF_EUI=dataDF[EUI_list]
	dataDF_EUI=dataDF_EUI.dropna()
	for EUI_label in EUI_list:
		if EUI_label in dataDF_EUI.columns:
			EUI_dist(dataDF_EUI,label=EUI_label)
	#shows the distribution of each feature
	#main_feature_distribution(dataDF)
	plt.show()
	return mis_val_table_ren_columns

def standard_report(dataDF,building,contents='all'):
	"""produce a standard reports.
	"""
	general_items={}
	m=dataDF.shape[0]
	# rank based on source EUI

	#building ranking with weather normalized EUI ('WNEUI') which only contains 
	#heating and cooling. 

	EUI_list=['EUI','HEUI','CEUI','WNEUI','TNEUI']
	dataDF_EUI=dataDF[EUI_list]
	dataDF_EUI=dataDF_EUI.dropna()
	EUI_rank_dict={}
	for EUI_label in EUI_list:
		if EUI_label in building.index:
			EUI_dist(dataDF_EUI,label=EUI_label,building_EUI=building[EUI_label])
			percentage_EUI=EUI_rank(dataDF_EUI,label=EUI_label,building_EUI=building[EUI_label])
			EUI_rank_dict[EUI_label]=percentage_EUI
	print('EUI_rank_dict',EUI_rank_dict)
	plt.show()
	
	#the position of end uses including heating, cooling, lighting, equipment and others.

	#the position of main features, such as external wall, windows.

def highlowReport(building,dataDF,contents='all'):
	"""report competition between high and low performance building.
	"""
	pass
	


def main_feature_distribution(dataDF):
	"""shows the distribution of continuous features using matplotlib.
	"""
	#mainFeatures=db.Database.mainFeatures
	
	for feature in mainFeatures:
		fig,ax=plt.subplots()
		ax=dataDF[feature].hist()
		ax.set_xlabel(feature)
		ax.set_ylabel('Building Number')
		plt.show()

def EUI_dist(dataDF, label='EUI', building_EUI=None):
	"""shows the EUI distribution.
	Parameters:
	----------
	dataDF, a DataFrame object contains the data.
	label, the type of EUI for the distribution analsis. Candidate items include 
		HEUI, CEUI, WNEUI, TNEUI.
	"""
	dataDF=dataDF[dataDF[label]>0][dataDF[label]<1000]
	figureEUI=plt.figure()
	figureEUI.set_figheight(10)
	figureEUI.set_figwidth(15)
	#the distribution of EUI using histogram
	ax1=figureEUI.add_subplot(2,2,1)
	ax1.hist(dataDF[label].values,bins=100)

	EUI_25P_value=dataDF[label].describe()['25%']
	EUI_75P_value=dataDF[label].describe()['75%']
	if building_EUI:
		ax1.axvline(building_EUI,color='y')
		#ax1.annotate('This building',(building_EUI,1),color='y')
	ax1.axvline(EUI_25P_value,color='r')
	ax1.axvline(EUI_75P_value,color='r')
	ax1.annotate('25%',(EUI_25P_value,1),color='r')
	ax1.annotate('75%',(EUI_75P_value,1),color='r')
	ax1.set_xlabel(str(label))
	ax1.set_ylabel(r'Number of buildings')
	#the distribution of log2(eui) using histogram
	ax2=figureEUI.add_subplot(2,2,2)
	ax2.hist(np.log2(dataDF[label].values),bins=100)

	EUI_25P_log=np.log2(dataDF[label].describe()['25%'])
	EUI_75P_log=np.log2(dataDF[label].describe()['75%'])
	if building_EUI:
		building_EUI_log=np.log2(building_EUI)
		ax2.axvline(building_EUI_log,color='y')
		#ax2.annotate('This building',(building_EUI_log,1),color='y')
	ax2.axvline(EUI_25P_log,color='r')
	ax2.axvline(EUI_75P_log,color='r')
	ax2.annotate('25%',(EUI_25P_log,1),color='r')
	ax2.annotate('75%',(EUI_75P_log,1),color='r')
	ax2.set_xlabel('$log_2$({0})'.format(label))
	ax2.set_ylabel('Number of buildings')
	return figureEUI

def EUI_rank(dataDF,label='EUI', building_EUI=None):
	"""show the ranks of the target building.
	Parameters:
	----------
	dataDF, a DataFrame object contains the data.
	label, the type of EUI for the distribution analsis. Candidate items include 
		HEUI, CEUI, WNEUI, TNEUI.
	"""
	m=dataDF.shape[0]
	n=np.searchsorted(np.sort(dataDF[label].values), building_EUI)
	percentage_EUI=n/m
	return percentage_EUI




def missing_values_table(dataDF,feature_list=None):
	"""summarize the missing values of each columns. 
		This function comes from Will Koehrsen(at https://towardsdatascience.com/a-complete-machine-learning-walk-through-in-python-part-one-c62152f39420)
	Parameters:
	----------
	df, the dataset.

	Return:
	----------
	mis_val_table_ren_columns, a DataFrame object that contains the information
		of missing data.
	"""
	# Total missing values
	if feature_list:
		df=dataDF[feature_list]
	else:
		df=dataDF
	mis_val = df.isnull().sum()
	# Percentage of missing values
	mis_val_percent = 100 * df.isnull().sum() / len(df)
	# Make a table with the results
	mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)

	# Rename the columns
	mis_val_table_ren_columns = mis_val_table.rename(
	columns = {0 : 'Missing Values', 1 : '% of Total Values'})

	# Sort the table by percentage of missing descending
	mis_val_table_ren_columns = mis_val_table_ren_columns[
	    mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
	'% of Total Values', ascending=False).round(1)

	# Print some summary information
	print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"      
	    "There are " + str(mis_val_table_ren_columns.shape[0]) +
	      " columns that have missing values.")

	# Return the dataframe with missing information
	return mis_val_table_ren_columns

