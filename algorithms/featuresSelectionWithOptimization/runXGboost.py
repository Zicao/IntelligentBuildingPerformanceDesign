#!/usr/bin/env python

# Read DAKOTA parameters file (aprepro or standard format) and call a
# Python module rosenbrock for analysis.  Uses same rosenbrock.py as
# linked case for consistency.

# DAKOTA will execute this script as
#   rosenbrock_bb.py params.in results.out
# so sys.argv[1] will be the parameters file and
#    sys.argv[2] will be the results file to return to DAKOTA

# necessary python modules
import sys
import re
import os
import time
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
import xgboost as xgb
# ----------------------------
# Parse DAKOTA parameters file
# ----------------------------

# setup regular expressions for parameter/label matching
e = '-?(?:\\d+\\.?\\d*|\\.\\d+)[eEdD](?:\\+|-)?\\d+' # exponential notation
f = '-?\\d+\\.\\d*|-?\\.\\d+'                        # floating point
i = '-?\\d+'                                         # integer
value = e+'|'+f+'|'+i                                # numeric field
tag = '\\w+(?::\\w+)*'                               # text tag field

# regular expression for aprepro parameters format
aprepro_regex = re.compile('^\s*\{\s*(' + tag + ')\s*=\s*(' + value +')\s*\}$')
# regular expression for standard parameters format
standard_regex = re.compile('^\s*(' + value +')\s+(' + tag + ')$')

# open DAKOTA parameters file for reading
paramsfile = open(sys.argv[1], 'r')

# extract the parameters from the file and store in a dictionary
paramsdict = {}
for line in paramsfile:
    m = aprepro_regex.match(line)
    if m:
        paramsdict[m.group(1)] = m.group(2)
    else:
        m = standard_regex.match(line)
        if m:
            paramsdict[m.group(2)] = m.group(1)

paramsfile.close()



# execute the rosenbrock analysis as a separate Python module
indexList=[]
i=0
for key,value in paramsdict.items():
    if re.search('1.000',value) and re.search('X\d',key):
        indexList.append(i)
        i+=1
    elif re.search('X\d',key):
        i+=1
print('indexList',indexList)

from random import randint
if len(indexList)==0:
    indexList.append(randint(0, 20))

def get_auc(indexList):

    CBECS_mat= pd.read_pickle('C:\\Users\\tzcha\\Documents\\aibpd\\application\\CBECS_4heating_clf.plk')
    y=CBECS_mat['heatingLevel']

    allFeature=['buildingAreaCategory','buildingShape','censusRegion','climateZone','HDD65',
                    'HVACUpgrade','insulationUpgrade','MAINHT','MONUSEC',
                      'OWNTYPE', 'region','RENWLL','roofConstruction','wallConstruction',
                        'WHOPPR','WINTYP','WKHRSC','WWR','yearOfConstruction']
    al=np.array(allFeature)
    al_iter=list(al[indexList])
    mainFeaturesCBECS_Categorical=[]
    mainFeaturesCBECS_numeric=[]
    mainFeaturesCBECS_Categorical1=['buildingAreaCategory','buildingShape',
                    'censusRegion','climateZone','HVACUpgrade',
                    'insulationUpgrade','MAINHT','MONUSEC','OWNTYPE', 
                    'region','RENWLL','roofConstruction','wallConstruction',
                        'WHOPPR','WINTYP','WKHRSC']
    mainFeaturesCBECS_numeric1=['HDD65','WWR','yearOfConstruction']
    for feature in al_iter:
        if feature in mainFeaturesCBECS_numeric1:
            mainFeaturesCBECS_numeric.append(feature)
        elif feature in mainFeaturesCBECS_Categorical1:
            mainFeaturesCBECS_Categorical.append(feature)

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])
    numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])
    preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer,mainFeaturesCBECS_numeric),
            ('cat', categorical_transformer,mainFeaturesCBECS_Categorical)])

    X=preprocessor.fit_transform(CBECS_mat[al_iter])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)



    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    param = {'max_depth': 2, 'eta': 0.8, 'verbosity': 1, 'objective': 'binary:logistic','gamma':0.5}
    param['nthread'] = 4
    param['eval_metric'] = 'auc'
    evallist = [(dtrain, 'train'),(dtest, 'test')]
    num_round = 20

    bst = xgb.train(param,dtrain, num_round,evallist,
            callbacks=[xgb.callback.print_evaluation(show_stdv=False),
            xgb.callback.early_stop(3)])
    return bst.best_score
def logregobj(preds, dtrain):
    labels = dtrain.get_label()
    preds = 1.0 / (1.0 + np.exp(-preds))
    grad = preds - labels
    hess = preds * (1.0 - preds)
    return grad, hess
def evalerror(preds, dtrain):
    labels = dtrain.get_label()
    return 'error', float(sum(labels != (preds > 0.0))) / len(labels)

def get_auc_cv(indexList):
    CBECS_mat= pd.read_pickle('C:\\Users\\tzcha\\Documents\\aibpd\\application\\CBECS_4heating_clf.plk')
    allFeature=['buildingAreaCategory','buildingShape','censusRegion','climateZone','HDD65',
                    'HVACUpgrade','insulationUpgrade','MAINHT','MONUSEC',
                      'OWNTYPE', 'region','RENWLL','roofConstruction','wallConstruction',
                        'WHOPPR','WINTYP','WKHRSC','WWR','yearOfConstruction']
    al=np.array(allFeature)
    al_iter=list(al[indexList])
    mainFeaturesCBECS_Categorical=[]
    mainFeaturesCBECS_numeric=[]
    mainFeaturesCBECS_Categorical1=['buildingAreaCategory','buildingShape',
                    'censusRegion','climateZone','HVACUpgrade',
                    'insulationUpgrade','MAINHT','MONUSEC','OWNTYPE', 
                    'region','RENWLL','roofConstruction','wallConstruction',
                        'WHOPPR','WINTYP','WKHRSC']
    mainFeaturesCBECS_numeric1=['HDD65','WWR','yearOfConstruction']
    for feature in al_iter:
        if feature in mainFeaturesCBECS_numeric1:
            mainFeaturesCBECS_numeric.append(feature)
        elif feature in mainFeaturesCBECS_Categorical1:
            mainFeaturesCBECS_Categorical.append(feature)

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))])
    numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])
    preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer,mainFeaturesCBECS_numeric),
            ('cat', categorical_transformer,mainFeaturesCBECS_Categorical)])
    
    X=preprocessor.fit_transform(CBECS_mat[al_iter])
    y=CBECS_mat['heatingLevel']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test,label=y_test)
    
    param = {'max_depth': 2, 'eta': 0.8, 'verbosity': 1, 'objective': 'binary:logistic','gamma':0.5}
    param['nthread'] = 4
    param['eval_metric'] = 'auc'
    evallist = [(dtrain, 'train'),(dtest, 'test')]
    num_round = 10
    
    df=xgb.cv(param, dtrain, num_round, nfold=5, metrics={'auc'},seed=0, obj=logregobj, feval=evalerror)
    auc = np.max(df['test-auc-mean'].values)
    return auc
auc=get_auc_cv(indexList)
print('auc',auc)
# ----------------------------
# Return the results to DAKOTA
# ----------------------------

# write the results.out file for return to DAKOTA
# this example only has a single function, so make some assumptions;
# not processing DVV
outfile = open('results.out.tmp', 'w')

# write functions
outfile.write(str(1-auc))
outfile.close()

# move the temporary results file to the one DAKOTA expects
import shutil
shutil.move('results.out.tmp', sys.argv[2])
#os.system('mv results.out.tmp ' + sys.argv[2])