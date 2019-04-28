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
print(indexList)

from random import randint
if len(indexList)==0:
    indexList.append(randint(0, 25))
CBECS_mat=np.load('CBECS_DF_clf_HT.npy')
X=CBECS_mat[:,indexList]
Y=CBECS_mat[:,-1]

m=CBECS_mat.shape[0]
n=int(0.8*m)
Y=Y.reshape(m,1)
Y=Y.astype('int')
'''
from sklearn.ensemble import BaggingClassifier
clf_bag=BaggingClassifier()
clf_bag.fit(X[:n,indexList],Y[:n])
error=1-clf_bag.score(X[n:m,indexList],Y[n:m])

from sklearn.tree import DecisionTreeClassifier
clf_dt=DecisionTreeClassifier()
clf_dt.fit(X[:n,indexList],Y[:n])
error=1-clf_dt.score(X[n:m,indexList],Y[n:m])

clf = SVC(gamma='auto')
clf.fit(X[:n,indexList],Y[:n]) 
error=1-clf.score(X[n:m,indexList],Y[n:m])
'''
from sklearn.svm import SVC

from sklearn.model_selection import KFold
kf = KFold(n_splits=5)
errorList=[]
for train_index, test_index in kf.split(X,Y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = Y[train_index], Y[test_index]
    clf = SVC(gamma='auto')
    clf.fit(X_train,y_train) 
    error=1-clf.score(X_test,y_test)
    errorList.append(error)
error=np.mean(errorList)
# ----------------------------
# Return the results to DAKOTA
# ----------------------------

# write the results.out file for return to DAKOTA
# this example only has a single function, so make some assumptions;
# not processing DVV
outfile = open('results.out.tmp', 'w')

# write functions
outfile.write(str(error))
outfile.close()

# move the temporary results file to the one DAKOTA expects
import shutil
shutil.move('results.out.tmp', sys.argv[2])
#os.system('mv results.out.tmp ' + sys.argv[2])