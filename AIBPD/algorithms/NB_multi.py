import numpy as np
from sklearn.naive_bayes import MultinomialNB
from IntelligentBuildingPerformanceDesign.AIBPD.data.database import Database
from IntelligentBuildingPerformanceDesign.AIBPD.data.preprocessing import PreprocessingCBECS
import pandas as pd
import math
def data_preprocess_BN_Designer(similarBldDF):
		'''

		'''

		coolLoadList=[]
		coolLoadList=[]
		equalSizeBin2=[1,2]
		equalSizeBin4=[1,2,3,4]
		equalSizeBin5=[1,2,3,4,5]
		similarBldDF['principleActivityN']=pd.qcut(similarBldDF['principleActivity'],5,labels=equalSizeBin5)
		#similarBldDF['principleActivity']#np.where(similarBldDF['principleActivity']==1, 1, 0)
		
		similarBldDF['climateZoneN']=pd.cut(similarBldDF['climateZone'],[0,1,2,7],labels=[1,2,3])
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
		return similarBldDF

database=Database()
CBECS2012DF=database.select('CBECS2012')
preprocess=PreprocessingCBECS()
CBECS2012DF=CBECS2012DF[CBECS2012DF['CDD65']>500]
CBECS2012DF=preprocess.forHECLClf(CBECS2012DF)
candidateDF=data_preprocess_BN_Designer(CBECS2012DF)
candidateDF=candidateDF.dropna()
m,n=candidateDF.shape
m09=int(0.9*m)

#proposed method
X_train_new=candidateDF[:m09][candidateDF['HECS']<=1][['climateZoneN','COOLLOAD','principleActivityN','MAINCLN']].values
y_train_new=candidateDF[:m09][candidateDF['HECS']<=1][['HECS']].values
X_test_new=candidateDF[m09:][candidateDF['HECS']<=1][['climateZoneN','COOLLOAD','principleActivityN','MAINCLN']].values
y_test_new=candidateDF[m09:][candidateDF['HECS']<=1][['HECS']].values

clf_new=MultinomialNB()
clf_new.fit(X_train_new,y_train_new)
print('score of new method',clf_new.score(X_test_new,y_test_new))

#mimic old method
X_train=candidateDF[:m09][['climateZoneN','COOLLOAD','principleActivityN']].values
y_train=candidateDF[:m09][['MAINCLN']].values
X_test=candidateDF[m09:][['climateZoneN','COOLLOAD','principleActivityN']].values
y_test=candidateDF[m09:][['MAINCLN']].values

clf = MultinomialNB()
clf.fit(X_train,y_train)
print('score of old method',clf.score(X_test,y_test))
#test the results of this method

#[candidateDF['HECS']<=1]
n=0
for i in range(X_test.shape[0]):
	CL=clf.predict(X_test[i,:3].reshape(1,3))
	if CL[0]==X_test[i,3]:
		n+=1
print('precision with test data',n/X_test.shape[0])
'''