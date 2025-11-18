import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pykrige.ok import OrdinaryKriging

keren = r"rhoapparent/data.xlsx"
data = pd.read_excel(keren)

a = np.array(data["A"])
b = np.array(data["B"])
m = np.array(data["M"])
n = np.array(data["N"])
v = np.array(data["V"])
i = np.array(data["I"])
j = 10
dv = np.diff(v, prepend=0)
method = 'S'

class Konfigurasi :
    def __init__(self,j, a, b, m, n, v, i, dv):
        self.a = a
        self.b = b
        self.m = m
        self.n = n
        self.v = v
        self.i = i
        self.dv = dv
        self.j = j
    
    
    def S(a,b,m,n):
        return np.pi*(((a*b)**2 + (m*n)**2)/2*m*n)
    def W(j) :
        return 2*np.pi*j
    def G(A,M,B,N):
        return np.pi*((1/(A*M))+(1/(B*N))-(1/(B*M))-(1/(A*N)))
    
def R(dv,i):
    return dv / i
def rho_a(K,R):
    return K * R

if method == 'S':
    data["K"] = [Konfigurasi.S(a[i], b[i], m[i], n[i]) for i in range(len(a))]
elif method == 'W':
    data["K"] = [Konfigurasi.W(j) for i in range(len(a))]
elif method == 'G':
    data["K"] = [Konfigurasi.G(a[i], m[i], b[i], n[i]) for i in range(len(a))]

data["R"] = R(dv, i)
data["rho_a"] = rho_a(data["K"], data["R"])


x = np.array(data["A"])
y = np.array(data["B"])
z = np.array(data["rho_a"])

OK = OrdinaryKriging(
    x,y,z,
    variogram_model='spherical',  # model: 'linear', 'power', 'gaussian', 'exponential', dll
    verbose=False,
    enable_plotting=False
)

gridx = np.linspace(min(x), max(x), 100)
gridy = np.linspace(min(y), max(y), 100)
z_pred, ss = OK.execute('grid', gridx, gridy)
plt.figure(figsize=(8,6))
plt.contourf(gridx, gridy, z_pred, cmap='viridis')
plt.scatter(x, y, c=z, edgecolor='k', s=80, cmap='viridis')
plt.colorbar(label='Nilai Prediksi (Z)')
plt.title('Peta Hasil Ordinary Kriging')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()


