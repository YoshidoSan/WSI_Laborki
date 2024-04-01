import matplotlib.pyplot as plt
import cec2017
import numpy as np
from cec2017.functions import f1,f2,f3
import math
from autograd import grad
np.set_printoptions(precision=3)
#DIM2   f1-10^-8
#DIM10  f1-
#=============funkcja i gradient=============================================
def yf(x):
    return pow((x[0] + 2 * x[1] - 7), 2) + pow((2 * x[0] + x[1] - 5), 2)
dim = 2
#yf = f3
grad_fct = grad(yf)
#===========dane do wykresu==================================================
MAX_X = 100
PLOT_STEP = 0.1
x_arr = np.arange(-MAX_X, MAX_X, PLOT_STEP)
y_arr = np.arange(-MAX_X, MAX_X, PLOT_STEP)
X, Y = np.meshgrid(x_arr, y_arr)
Z = np.empty(X.shape)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i, j] = yf(np.array([X[i, j], Y[i, j]]))
#=====================definicja zmiennych====================================
how_many=0
x_k = np.random.uniform(-MAX_X, MAX_X, size=dim)
beta = 0.05
#beta = pow(10,-8)
i = 0
max_i = 500
error= 0.001
ar_points = []
#================pętla algorytmu=============================================
#q= yf(x_k)
ar_points.append(x_k)
print("x: ",x_k)
print('q(x) = %.6f' % yf(x_k))
while i < max_i:
    x_kp1 = x_k - beta * grad_fct(x_k)
    print("Iteracja", i)
    for j in range(dim):
        if abs(x_k[j]-x_kp1[j]) <= error:
            how_many+=1
        if how_many == dim:
            i = max_i
            how_many=0
        elif j == dim-1:
            how_many = 0
    x_k = x_kp1
    ar_points.append(x_k)
    i = i + 1
    print("x: ", x_k)
    print('q(x) = %.6f' % yf(x_k))
#==============strzałka======================================================
plt.contour(X, Y, Z, 30)
for i in range(len(ar_points)-1):
    plt.arrow(ar_points[i][0],ar_points[i][1],ar_points[i+1][0]-ar_points[i][0],ar_points[i+1][1]-ar_points[i][1],head_width=1,head_length=1,fc='k',ec='r')
#======================pokazanie wykresu=====================================
plt.title(f'Wartość funkcji: {round(yf(x_k),2)}, beta: {beta}, x_0: {x_k}')
print("Minimum: ", x_k)
plt.show()

