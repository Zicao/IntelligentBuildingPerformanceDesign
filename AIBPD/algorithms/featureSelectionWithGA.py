#run decision tree model for predicting high performance building
#receive array of measures

from sklearn import tree

CBECS_mat=np.load()
X=CBECS_mat[:,:-1]
y=CBECS_mat[:,:-1]


clf_dt=tree.DecisionTreeClassifier()
clf_dt.fit(X[:n,:],Y[:n])
Y_dt=clf_dt.predict(X[n:m,:])
print(clf_dt.score(X[n:m,:],Y[n:m]))