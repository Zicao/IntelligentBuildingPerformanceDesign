from pyswarms.discrete.binary import BinaryPSO
import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from pyswarms.utils.functions import single_obj as fx
# Change directory to access the pyswarms module

def objectiveFun(CBECS_array):
	indexList=[]
	i=0
	#print(CBECS_array)
	for index in CBECS_array:
		if index==1:
			indexList.append(i)
		i+=1
	#print(indexList)
	
	CBECS_mat=np.load('CBECS_DF_clf.npy')
	X=CBECS_mat[:,indexList]
	Y=CBECS_mat[:,-1]

	m=CBECS_mat.shape[0]
	n=int(0.8*m)
	Y=Y.reshape(m,1)
	Y=Y.astype('int')

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
	return error

def f(x):
    """Higher-level method to do classification in the
    whole swarm.

    Inputs
    ------
    x: numpy.ndarray of shape (n_particles, dimensions)
        The swarm that will perform the search

    Returns
    -------
    numpy.ndarray of shape (n_particles, )
        The computed loss for each particle
    """
    n_particles = x.shape[0]
    j = [objectiveFun(x[i]) for i in range(n_particles)]
    return np.array(j)

def rosenbrock_with_args(x, a, b, c=0):
    print(x)
    f = (a - x[:, 0]) ** 2 + b * (x[:, 1] - x[:, 0] ** 2) ** 2 + c+x[:,2]
    return f

if __name__ == '__main__':
	import sys
# Change directory to access the pyswarms module
	sys.path.append('../')
	print('Running on Python version: {}'.format(sys.version))
	options = {'c1': 0.5, 'c2': 0.3, 'w':0.9,'k':3,'p':2}

	optimizer=BinaryPSO(n_particles=10, dimensions=26, options=options)
	
	cost, pos = optimizer.optimize(f, print_step=1, iters=1500, verbose=3)
	print(pos)