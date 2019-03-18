import pomegranate as pm
import numpy as np
import math
import pandas as pd
class BN4CL():
	BN4CLfitted=None
	BN4CL_Designer=None

	def __init__(self):
		pass

	def predict(self, building):
		'''
		Predict the most-likely high performance cooling system for the proposed building.
		Args:
			proposedBuilding, a two-dimensional list.
		Example:
			proposedBuilding=[[1,11,1,None,2,1,1]] #(climateZone,COOLLOAD,principleActivity,MAINCl,CDD65,COOLP,HECS)
		'''
		proposedBuilding=building.building
		proposedBuildingList=[]
		proposedBuildingList.append(proposedBuilding['climateZone'])
		proposedBuildingList.append(proposedBuilding['COOLLOAD'])
		proposedBuildingList.append(proposedBuilding['principleActivity'])
		proposedBuildingList.append(None)
		proposedBuildingList.append(proposedBuilding['CDD65'])
		proposedBuildingList.append(proposedBuilding['COOLP'])
		proposedBuildingList.append(proposedBuilding['HECS'])

		predictionResult=self.BN4CLfitted.predict([proposedBuildingList])
		print("The most-likely high performance cooling system for the proposed building is",predictionResult[0][3])
	
	def probability(self,buildingList):
		'''
		Predict 
		Args:
			buildingList, two dimensional list object
		Example:
			buildingList=[[1,11,1,3.0,0,1,1],[1,11,1,2.0,0,1,1],[1,11,1,1.0,0,1,1]]
		'''
		probabilityofCLSystems=self.BN4CLfitted.probability(probabilityList)
		print(probabilityofCLSystems)
	def data_preprocess_BN(self,similarBldDF):
		'''

		'''
		coolLoadList=[]
		equalSizeBin2=[1,2]
		equalSizeBin4=[1,2,3,4]
		equalSizeBin5=[1,2,3,4,5]
		similarBldDF['principleActivityN']=pd.qcut(similarBldDF['principleActivity'],5,labels=equalSizeBin5)
		#similarBldDF['principleActivity']#np.where(similarBldDF['principleActivity']==1, 1, 0)
		
		similarBldDF['climateZoneN']=pd.cut(similarBldDF['climateZone'],[0,1,2,3,7],labels=[1,2,3,4])
		similarBldDF['CDD65N']=pd.qcut(similarBldDF['CDD65'],5,labels=equalSizeBin5)
		similarBldDF['COOLPN']=pd.cut(similarBldDF['COOLP'],[10,90,100],labels=equalSizeBin2)
		similarBldDF['MAINCLN']=similarBldDF['MAINCL']
		similarBldDF['MAINCLN'][np.abs(similarBldDF['MAINCLN'])<1]=0
		similarBldDF['MAINCLN'][np.abs(similarBldDF['MAINCLN'])>3]=4
		similarBldDF=similarBldDF.dropna()
		for index, row in similarBldDF.iterrows():
			if row['climateZone']==1:
				coolLoadList.append(int(math.log(row['buildingArea']*0.8)))
			elif row['climateZone']==2 or row['climateZone']==5 or row['climateZone']==7:
				coolLoadList.append(int(math.log(row['buildingArea']*1.0)))
			elif row['climateZone']==3:
				coolLoadList.append(int(math.log(row['buildingArea']*1.2)))
			else:
				coolLoadList.append(int(math.log(row['buildingArea']*1.0)))
		similarBldDF['COOLLOAD']=coolLoadList
		del coolLoadList
		return similarBldDF[['ID','climateZoneN','COOLLOAD','principleActivityN','MAINCLN','CDD65N','COOLPN','HECS']]


	def attributeDistribution(self,similarBldDF):
		'''
		Calculate the distribution of different attributes, for example climateZone, pricipleActivity...
		Args:
			similarBldDF, a pandas DataFrame object includes a group of building similar to the proposed 
				building.
		'''
		similarBldDF=self.data_preprocess_BN(similarBldDF)
		m,n=similarBldDF.shape
		similarBldDF=similarBldDF.dropna()
		
		climateZoneNDict=similarBldDF.groupby('climateZoneN').count()['ID'].to_dict()
		COOLPNDict=similarBldDF.groupby('COOLPN').count()['ID'].to_dict()
		CDD65NDict=similarBldDF.groupby('CDD65N').count()['ID'].to_dict()
		COOLLOADDict=similarBldDF.groupby('COOLLOAD').count()['ID'].to_dict()
		MAINCLDict=similarBldDF.groupby('MAINCLN').count()['ID'].to_dict()
		principleActivityNDict=similarBldDF.groupby('principleActivityN').count()['ID'].to_dict()

		#MAINCLDist=similarBldDF.groupby('MAINCL').count()['ID'].to_dict()
		#MAINHTDist=similarBldDF.groupby('MAINHT').count()['ID'].to_dict()
	    
	    
		climateZoneDictN=self.dictRatio(climateZoneNDict,m)
		COOLPNDictN=self.dictRatio(COOLLOADDict,m)
		principleActivityNDictN=self.dictRatio(principleActivityNDict,m)
		CDD65NDictN=self.dictRatio(CDD65NDict,m)
		COOLPNDictN=self.dictRatio(COOLPNDict,m)
		COOLLOADDictN=self.dictRatio(COOLLOADDict,m)
		MAINCLDictN=self.dictRatio(MAINCLDict,m)
		

		#MAINCLDistN=self.dictRatio(MAINCLDist,m)

		#Form the conditional probability table.
		MAINCLCPT=[]
		for l in list(climateZoneDictN.keys()):#PUBLICIM
			for j in list(COOLLOADDictN.keys()):#coolload
				for k in list(principleActivityNDictN.keys()): #principleActivity
					for i in list(MAINCLDictN.keys()):#[0,1,2,3,4,5,6,7]
						MAINCLCPT.append([int(l),int(j),int(k),int(i),0.0])

		MAINCLCPTMat=np.mat(MAINCLCPT)
		#
		#similarBldDF['climateZone']=pd.to_numeric(similarBldDF['climateZone'], errors='coerce')
		similarBldDF=similarBldDF.dropna()
		
		#similarBldDF['climateZone']=similarBldDF['climateZone'].astype(int)
		#similarBldDF=similarBldDF[similarBldDF['climateZoneN']<=6][similarBldDF['climateZoneN']>=0]
		similarBldDF=similarBldDF.reindex(range(similarBldDF.shape[0]))
		for j01 in range(similarBldDF.shape[0]):
			for j02 in range(len(MAINCLCPT)):
				if MAINCLCPTMat[j02,0]==similarBldDF['climateZoneN'].iloc[j01] and \
				MAINCLCPTMat[j02,1]==int(similarBldDF['COOLLOAD'].iloc[j01]) and \
				MAINCLCPTMat[j02,2]==int(similarBldDF['principleActivityN'].iloc[j01]) and \
				MAINCLCPTMat[j02,3]==int(similarBldDF['MAINCLN'].iloc[j01]):
					MAINCLCPTMat[j02,4]+=1
	#MAINCLCPTList is used to calculate the conditional table
		MAINCLCPTMat[:,4]=MAINCLCPTMat[:,4]/m
		self.nonZeroPTable(MAINCLCPTMat)
		MAINCLCPTList=MAINCLCPTMat.tolist()

		HECSCPT=[]
		for i in list(climateZoneDictN.keys()): #climateZone
			for j in list(MAINCLDictN.keys()): #MAINCL
				for k in list(principleActivityNDictN.keys()):#principleActivityN
					for l in list(CDD65NDictN.keys()): #CDD65N
						for l2 in list(COOLPNDictN.keys()): #COOLPN
							for l3 in [0,1]:#High efficient cooling system
								HECSCPT.append([int(i),int(j),int(k),int(l),int(l2),int(l3),0.0])
		HECSCPTMat=np.mat(HECSCPT)

		for j11 in range(similarBldDF.shape[0]):
			for j12 in range(len(HECSCPT)):
				if HECSCPTMat[j12,0]==similarBldDF['climateZoneN'].loc[j11] and \
				HECSCPTMat[j12,1]==int(similarBldDF['MAINCLN'].loc[j11]) and \
				HECSCPTMat[j12,2]==int(similarBldDF['principleActivityN'].loc[j11]) and \
				HECSCPTMat[j12,3]==int(similarBldDF['CDD65N'].loc[j11]) and \
				HECSCPTMat[j12,4]==int(similarBldDF['COOLPN'].loc[j11]) and \
				HECSCPTMat[j12,5]==int(similarBldDF['HECS'].loc[j11]):
					HECSCPTMat[j12,6]+=1
		HECSCPTMat[:,6]=HECSCPTMat[:,6]/m
		self.nonZeroPTable(HECSCPTMat)
		HECSCPTList = HECSCPTMat.tolist()
	    
		print("BN for Main cooling equipment","climateZoneDictN",climateZoneDictN,"COOLLOADDictN",COOLLOADDict,"principleActivityNDictN",principleActivityNDictN)
		print("BN for High efficient building","MAINCLDictN",MAINCLDictN,"principleActivityNDictN",principleActivityNDictN,"CDD65NDictN",CDD65NDictN,"COOLPNDictN",COOLPNDictN)
		print("Distribution of cooling system",MAINCLDictN)
		return climateZoneDictN,COOLLOADDictN,principleActivityNDictN,MAINCLCPTList,MAINCLDictN,CDD65NDictN,COOLPNDictN,HECSCPTList
	
	def fit(self, similarBldDF):
		'''
		climate zone, Design cooling load and principle building activity are parents attributes of main cooling equipment.
		Census division, main cooling equipment, cooling degree days, percentage of building cooled are four parent attribute of high efficient building
		Attributes:
			similarBldDF, a pandas DataFrame object includes a group of building similar to the proposed 
				building.This object is used to train the Bayesian Network classifier.

		'''
		climateZoneDict,COOLLOADDict,principleActivityNDict,MAINCLCPTList,MAINCLDict,CDD65NDict,COOLPNDict,HECSCPTList=self.attributeDistribution(similarBldDF)

		climateZone=pm.DiscreteDistribution(climateZoneDict)
		designCoolingLoad=pm.DiscreteDistribution(COOLLOADDict)
		principleBuildingActivity=pm.DiscreteDistribution(principleActivityNDict)

		coolingDegreeDays = pm.DiscreteDistribution(CDD65NDict)
		percentageofBuildingCooled = pm.DiscreteDistribution(COOLPNDict)

		#MCE_CPT is the conditional probability table of main cooling equipment
		mainCoolingEquipmentCPT=pm.ConditionalProbabilityTable(MAINCLCPTList,[climateZone,designCoolingLoad,principleBuildingActivity])
		#HECS_CPT is the conditional probability table of high efficient cooling system.
		highEfficientCoolingSystemCPT=pm.ConditionalProbabilityTable(HECSCPTList,[climateZone,mainCoolingEquipmentCPT,principleBuildingActivity,\
	                                                                           coolingDegreeDays,percentageofBuildingCooled])
		
		#the first layer parent attributes
		p1_climateZone=pm.Node(climateZone,name="climateZone")#climateZone
		p1_COOLLOAD=pm.Node(designCoolingLoad,name="COOLLOAD")#COOLLOAD
		p1_principleActivity=pm.Node(principleBuildingActivity,name="principleActivity")#principleActivity

		#the second layer parent attributes
		#the main cooling equipment
		p2_MAINCL = pm.Node(mainCoolingEquipmentCPT,name="MAINCL")#
		p2_CDD65 = pm.Node(coolingDegreeDays,name="CDD65")
		p2_COOLP = pm.Node(percentageofBuildingCooled,name="COOLP")

		#high efficient cooling system
		p_HECS = pm.Node(highEfficientCoolingSystemCPT, name="highEfficientCoolingSystemCPT")

		#the Bayesian Network for the main cooling equipment
		modelMCE = pm.BayesianNetwork("Main cooling equipment")
		modelMCE.add_nodes(p1_climateZone,p1_COOLLOAD,p1_principleActivity,p2_MAINCL,p2_CDD65,p2_COOLP,p_HECS)
		modelMCE.add_edge(p1_climateZone,p2_MAINCL)
		modelMCE.add_edge(p1_COOLLOAD,p2_MAINCL)
		modelMCE.add_edge(p1_principleActivity,p2_MAINCL)
		modelMCE.add_edge(p1_climateZone,p_HECS)
		modelMCE.add_edge(p2_MAINCL,p_HECS)
		modelMCE.add_edge(p1_principleActivity,p_HECS)
		modelMCE.add_edge(p2_CDD65,p_HECS)
		modelMCE.add_edge(p2_COOLP,p_HECS)
		modelMCE.bake()
		self.BN4CLfitted=modelMCE

	def predict_test(self,similarBldDF):
		'''
		mimic the traditional method of selecting HVAC methods
		'''
		similarBldDF=self.data_preprocess_BN(similarBldDF)
		m=similarBldDF.shape[0]
		test_X=similarBldDF.values
		n=0
		for i in range(m):
			proposedBuildingList=list(test_X[i,1:7])
			proposedBuildingList.append(None)
			predictionResult=self.BN4CLfitted.predict([proposedBuildingList])
			if predictionResult[7]==1.0:
				n+=1
		print('Precision of BN = ',n/m)

	def dictRatio(self,dict1,m):
		'''
		adjust the value into decimal between [0,1]
		Args:
			dict1, a dict object.
		Examples:
			COOLLOADDictN={7: 2, 8: 25, 9: 45, 10: 42, 11: 58, 12: 80, 13: 28}
			m=2+25+45+42+58+80+28=280
			COOLLOADDictN=dictRatio(COOLLOADDictN)
			Now, COOLLOADDictN={7:0.00714,8: 0.08865, 9: 0.16071, 10: 0.1500, 11: 0.20714, \
								12: 0.2857, 13: 0.1000}
		'''
		dictKeys=list(dict1.keys())
		newdict={}
		for i in dictKeys:
			newdict[int(i)]=dict1[i]/m
		return newdict

	def nonZeroPTable(self, PTableMat):
		'''
		Bayesian Network classifier requires that the arguments should not be zero or none.
		To solve this problem, I use a small number 0.000000001 replacing 0
		Args:
			PTableMat, a matrix np object. 
		'''
		m,n=PTableMat.shape
		for i in range(m):
			if PTableMat[i,-1]==0:
				PTableMat[i,-1]=0.000000001
if __name__ == '__main_':
	pass