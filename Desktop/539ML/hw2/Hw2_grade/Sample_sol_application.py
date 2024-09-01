import math
import numpy as np
from Sample_sol_linear_regression import *
from sklearn.datasets import make_regression
# Note: please don't add any new package, you should solve this problem using only the packages above.
#-------------------------------------------------------------------------
'''
    Problem 2: Apply your Linear Regression
    In this problem, use your linear regression method implemented in problem 1 to do the prediction.
    Play with parameters alpha and number of epoch to make sure your test loss is smaller than 1e-2.
    Report your parameter, your train_loss and test_loss 
    Note: please don't use any existing package for linear regression problem, use your own version.
'''

#--------------------------

n_samples = 200
X,y = make_regression(n_samples= n_samples, n_features=4, random_state=1)
y = np.array(y).T
X = np.array(X)
Xtrain, Ytrain, Xtest, Ytest = X[::2], y[::2], X[1::2], y[1::2]

#########################################
## INSERT YOUR CODE HERE

paralist = []
for alpha in np.linspace(0,1.4,141):
    for iteration in range(1000):
        w_temp = train(Xtrain, Ytrain, alpha, iteration)
        test_loss = compute_L(compute_yhat(Xtest, w_temp), Ytest)
        if (test_loss < 1e-2):
            train_loss = compute_L(compute_yhat(Xtrain, w_temp), Ytrain)
            paralist.append([alpha, iteration, train_loss, test_loss])
            break

with open('paralist.txt', 'w') as f:
    for item in paralist:
        f.write(str(item[0])+'\t'+str(item[1])+'\t'+str(item[2])+'\t'+str(item[3])+'\n')






#########################################

