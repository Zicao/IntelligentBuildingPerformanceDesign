from aibpd.data.database import Database
from aibpd.data.preprocessing import PreprocessingCBECS
import numpy as np
import pandas as pd
db=Database()
CBECS_DF=db.select()
#preprocessing for regression
prep4eui=PreprocessingCBECS()
CBECS_DF=prep4eui.prep4EUIReg(CBECS_DF)
CBECS_DF=CBECS_DF[CBECS_DF['principleActivity']>=2][CBECS_DF['principleActivity']<3]
CBECS_DF=CBECS_DF.dropna()
CBECS_DF['MONUSEC']=pd.cut(CBECS_DF['MONUSE'],[0,6,9,10,13],labels=[1,2,3,4])
CBECS_DF['OCCUPYPC']=pd.cut(CBECS_DF['OCCUPYP'],5,labels=range(5))
CBECS_DF['HEATPC']=pd.cut(CBECS_DF['HEATP'],[-10,50,90,101],labels=[1,2,3])
CBECS_DF['MONUSEC']=CBECS_DF['MONUSEC'].astype('int')
CBECS_DF['OCCUPYPC']=CBECS_DF['OCCUPYPC'].astype('int')
CBECS_DF['HEATPC']=CBECS_DF['HEATPC'].astype('int')
CBECS_DF['EUI']=CBECS_DF['EUI'].astype('float')
featureList=['buildingAreaCategory','buildingShape','censusRegion','climateZone','ELHT1','HDD65',\
            'HEATPC','HVACUpgrade','insulationUpgrade','MAINCL','MAINHT','MONUSEC','numEmployeesCategory',\
             'numFloors','OCCUPYP','OPNWE',\
            'OWNTYPE', 'region','RENWLL','lightingUpgrade','roofConstuction','STUSED',\
            'OPEN24','wallConstruction',\
            'WHOPPR','WINTYP','WKHRSC','WWR','yrConstructionCategory','EUI']
corrMattDF=CBECS_DF[featureList]
column=featureList
print(corrMattDF.dtypes)
#feature selection
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score as acc
from mlxtend.feature_selection import SequentialFeatureSelector as sfs
X_train, X_test, y_train, y_test = train_test_split(
    corrMattDF.values[:,:-1],
    corrMattDF.values[:,-1],
    test_size=0.2,
    random_state=42)
y_train = y_train.ravel()
y_test = y_test.ravel()
#for j in range(1,25):
    #print('Training dataset shape:', X_train.shape, y_train.shape)
    #print('Testing dataset shape:', X_test.shape, y_test.shape)
    #j1=25-j
clf = svm.SVR(gamma=0.001, C=1.0, epsilon=0.2)
sfs1 = sfs(clf,
           k_features=20,
           forward=True,
           floating=False,
           verbose=2,
           scoring='r2',
           cv=5)

sfs1 = sfs1.fit(corrMattDF.values[:,:-1], corrMattDF.values[:,-1])
feat_cols = list(sfs1.k_feature_idx_)
print(feat_cols)