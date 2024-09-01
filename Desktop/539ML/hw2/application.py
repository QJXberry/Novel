import numpy as np
from linear_regression import *
from sklearn.datasets import make_regression

n_samples = 200
X, y = make_regression(n_samples=n_samples, n_features=4, random_state=1)
y = np.asmatrix(y).T
X = np.asmatrix(X)
Xtrain, Ytrain, Xtest, Ytest = X[::2, :], y[::2, :], X[1::2, :], y[1::2, :]

def epoch_result(alpha, n_epoch):
    w = train(Xtrain, Ytrain, alpha, n_epoch)
    train_loss = compute_L(compute_yhat(Xtrain, w), Ytrain)
    test_loss = compute_L(compute_yhat(Xtest, w), Ytest)
    print("alpha == ", alpha)
    print("train_loss == ", train_loss)
    print("test_loss == ", test_loss)
    print("n_epoch ==", n_epoch)
    print() # print a new line

alpha_values = [0.1] + list(np.arange(0.1, 0.8, 0.1))
epochs_values = range(50, 200, 25)

for alpha in alpha_values:
    for n_epoch in epochs_values:
        if alpha == 0.1 or (alpha in [0.1, 0.2, 0.3] and n_epoch in [50, 150, 300]):
            epoch_result(alpha, n_epoch)

"""
fixed_n_epoch = 100

# Vary alpha from 0.1 to 0.5
alpha_values = np.arange(0.1, 0.6, 0.1)

for alpha in alpha_values:
    # Use the fixed_n_epoch value for all iterations
    epoch_result(alpha, fixed_n_epoch)
    """



