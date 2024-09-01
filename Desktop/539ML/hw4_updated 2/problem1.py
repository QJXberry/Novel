import numpy as np
import math
 
#-----------------------------------------------------------------
# Forward Pass
#-----------------------------------------------------------------
 
def compute_z(x,W,b):
    z = np.dot(W,x) + b
    return z
 
def compute_a(z):
    z = z - np.max(z)
    for i in range(z.shape[0]):
        if (z[i] < -900).any():
            z[i] = 0
        else:
            z[i] = np.exp(z[i])
    a = z/np.sum(z)
    return a
 
def compute_L(a,y):
    try:
        L = -np.log(a[y])
        L = float(L)
    except:
        if a[y] == 0:
            L = 1000000
    return L
   
 
def forward(x,y,W,b):
    z = compute_z(x, W, b)
    a = compute_a(z)
    L = compute_L(a,y)
    return z, a, L
 
 
#-----------------------------------------------------------------
# Compute Local Gradients
#-----------------------------------------------------------------
 
def compute_dL_da(a, y):
    dL_da = np.zeros_like(a)
    dL_da[y] = -1 / (a[y] + 1e-10)
   
    return dL_da
 
 
def compute_da_dz(a):
    da_dz = np.zeros([a.shape[0], a.shape[0]])
    for i in range(a.shape[0]):
        for j in range(a.shape[0]):
            if i == j:
                da_dz[i][j] = a[i] * (1 - a[i])
            else:
                da_dz[i][j] = -a[i]*a[j]
 
    da_dz = np.array(da_dz)
    return da_dz
 
 
def compute_dz_dW(x,c):
    p = x.shape[0] # Assuming x is a 1D array of shape (p,)
    dz_dW = np.zeros((c, p))
    for i in range(c):
        dz_dW[i, :] = x.flatten()
    return dz_dW
 
def compute_dz_db(c):
    dz_db = np.array([1]*c)
    return dz_db
 
 
#-----------------------------------------------------------------
# Back Propagation
#-----------------------------------------------------------------
 
def backward(x, y, a):
    c = a.shape[0]
    dL_da = compute_dL_da(a, y)
    da_dz = compute_da_dz(a)
    dz_dW = compute_dz_dW(x, c)
    dz_db = compute_dz_db(c)
    return dL_da, da_dz, dz_dW, dz_db
 
def compute_dL_dz(dL_da,da_dz):
    dL_dz = np.dot(da_dz, dL_da)
    return dL_dz
 
 
def compute_dL_dW(dL_dz,dz_dW):
    dL_dW = dz_dW
    for i in range(dz_dW.shape[0]):
        dL_dW[i, :] = np.dot(dL_dW[i, :], dL_dz.item(i))
    return dL_dW
 
def compute_dL_db(dL_dz,dz_db):
    dL_db = dL_dz
    return dL_db
 
#-----------------------------------------------------------------
# gradient descent
#-----------------------------------------------------------------
def update_W(W, dL_dW, alpha=0.001):
    W = W - dL_dW*alpha
    return W
 
def update_b(b, dL_db, alpha=0.001):
    b = b - dL_db*alpha
    return b
#-----------------------------------------------------------------
# train
#-----------------------------------------------------------------
 
 
def train(X, Y, alpha=0.01, n_epoch=100):
    # number of features  IndexError: too many indices for array: array is 1-dimensional, but 2 were indexed
    p = X.shape[1]
    # number of classes
    c = max(Y) + 1
 
    # randomly initialize W and b
    W = np.random.rand(c, p)
    b = np.random.rand(c)
 
    for _ in range(n_epoch):
        # go through each training instance
        for x, y in zip(X, Y):
            z,a,L = forward(x, y, W, b)
 
            dL_da, da_dz, dz_dW, dz_db = backward(x, y, a)
 
            dL_dz = compute_dL_dz(dL_da, da_dz)
            dL_dW = compute_dL_dW(dL_dz,dz_dW)
            dL_db = compute_dL_db(dL_da, dz_db)
 
            W = update_W(W, dL_dW, alpha)
            b = update_b(b, dL_db, alpha)
    return W, b
 
def predict(Xtest, W, b):
    n = Xtest.shape[0]
    c = W.shape[0]
    Y = np.zeros(n, dtype=int) # Initialize Y as integer array
    P = np.zeros((n, c)) # Initialize P with correct shape
    for i, x in enumerate(Xtest):
           
        z = compute_z(x, W, b)
        a = compute_a(z)
        P[i] = a.T
        Y[i] = P[i].argmax()
       
    return Y, P
 
#-----------------------------------------------------------------
# gradient checking
#-----------------------------------------------------------------
 
def check_da_dz(z, delta=1e-7):
    c = z.shape[0] # number of classes
    da_dz = np.zeros((c, c))
    for i in range(c):
        for j in range(c):
            d = np.zeros(c)
            d[j] = delta
            da_dz[i, j] = (compute_a(z + d)[i] - compute_a(z)[i]) / delta
    return da_dz
 
def check_dL_da(a, y, delta=1e-7):
    c = a.shape[0] # number of classes
    dL_da = np.zeros(c) # initialize the vector as all zeros
    #print(dL_da)
    for i in range(c):
        d = np.zeros(c)
        d[i] = delta
        dL_da[i] = (compute_L(a + d, y) - compute_L(a, y)) / delta
    return dL_da
 
def check_dz_dW(x, W, b, delta=1e-7):
    c, p = W.shape # number of classes and features
    dz_dW = np.zeros((c, p))
    for i in range(c):
        for j in range(p):
            d = np.zeros((c, p))
            d[i, j] = delta
            dz_dW[i, j] = (compute_z(x, W + d, b)[i] - compute_z(x, W, b))[i] / delta
    return dz_dW
 
 
def check_dz_db(x, W, b, delta=1e-7):
    c, _ = W.shape # number of classes and features
    dz_db = np.zeros(c)
    for i in range(c):
        d = np.zeros(c)
        d[i] = delta
        dz_db[i] = (compute_z(x, W, b + d)[i] - compute_z(x, W, b)[i]) / delta
    return dz_db
 
def check_dL_dW(x,y,W,b,delta=1e-7):
    c, p = W.shape
    dL_dW = np.zeros((c, p))
    for i in range(c):
        for j in range(p):
            d = np.zeros((c, p))
            d[i, j] = delta
            dL_dW[i, j] = (forward(x, y, W + d, b)[-1] - forward(x, y, W, b)[-1]) / delta
    return dL_dW
 
def check_dL_db(x,y,W,b,delta=1e-7):
    c, p = W.shape
    dL_db = np.asmatrix(np.zeros((c,1)))
    for i in range(c):
        d = np.asmatrix(np.zeros((c,1)))
        d[i] = delta
        dL_db[i] = ( forward(x,y,W,b+d)[-1] - forward(x,y,W,b)[-1] ) / delta
    return dL_db
