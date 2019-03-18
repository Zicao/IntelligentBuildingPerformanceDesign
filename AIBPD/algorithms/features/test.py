import numpy as np
from sklearn.ensemble import BaggingClassifier
from sklearn.svm import SVC
CBECS_array=[1,0 ,0 ,0, 1 ,0 ,0,1 ,0, 1, 0,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0, 1, 0, 0 ,1 ,0 ,0 ,0]
indexList=[]
i=0
#print(CBECS_array)
for index in CBECS_array:
    if index==1:
        indexList.append(i)
    i+=1
print(indexList)
indexList=[3, 7, 9 ,12,13,14,17,18,19 20,23]
#indexList=[0,3,4,5,7,9,12,14,20,24,25]
CBECS_mat=np.load('CBECS_DF_clf.npy')
X=CBECS_mat[:,indexList]
Y=CBECS_mat[:,-1]

m=CBECS_mat.shape[0]
n=int(0.8*m)
Y=Y.reshape(m,1)
Y=Y.astype('int')
'''
clf_bag=BaggingClassifier()
clf_bag.fit(X[:n,indexList],Y[:n])
error=1-clf_bag.score(X[n:m,indexList],Y[n:m])'''
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
print(error)