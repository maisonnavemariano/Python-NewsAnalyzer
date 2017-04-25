import numpy as np
from numpy.linalg import svd
from numpy import diag

m = np.zeros(shape=(4,9))

m[0]=[+0.00,+0.00,+0.23,+0.00,+0.00,+0.10,+0.00,+0.00,+0.46]
m[1]=[+0.00,+0.17,+0.00,+0.00,+0.00,+0.07,+0.35,+0.35,+0.00]
m[2]=[+0.28,+0.14,+0.00,+0.28,+0.28,+0.06,+0.00,+0.00,+0.00]
m[3]=[+0.00,+0.00,+0.69,+0.00,+0.00,+0.00,+0.00,+0.00,0.00]
coef = 0

print(str(m))
u,sigma,vt = svd(m, full_matrices = False)
# sigma es un vector de valores singulares de M
for i in range(1,coef+1):
    sigma[-i] = 0
    sigma[-i] = 0
#  eliminamos los dos ultimos valores singulares (los dos menos significativos)
sigma = np.diag(sigma)
# np.diag(sigma) construye la matriz con todos ceros menos en la diagonal.
print("descomposicion")

print("u x sigma x vt : "+str(u.shape)+" x "+str(sigma.shape)+" x "+str(vt.shape))
print(str(sigma))
# la matrix reconstruida es:  np.dot(np.dot(u,sigma), vt)
print(str(np.dot(np.dot(u,sigma), vt)))
#print(str(vt))