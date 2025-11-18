import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pykrige.ok import OrdinaryKriging

keren = r"C:\Users\ASUS\Desktop\code angjay\rhoapparent\BackEnd\data.xlsx"
data = pd.read_excel(keren)

a = np.array(data["A"])
b = np.array(data["B"])
m = np.array(data["M"])
n = np.array(data["N"])
v = np.array(data["V"])
i = np.array(data["I"])
dv = np.diff(v, prepend=0)
method =  str(input("Masukin metode K (S, W, G, WS): ")).upper()

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
    def WS(a,b,m,n) :
        am = m-a
        bn = b-n
        mn = n-m 
        A = am
        N = mn/A
        return np.pi*A*(N+1)*(N+2)
    def S(a,b,m,n):
        return np.pi * ( ((a*b)**2 + (m*n)**2) / (2 * m * n) )
    def W(a,b) :
        j = a-b
        return 2*np.pi*j
    def G(A,M,B,N):
        return np.pi*((1/(A*M))+(1/(B*N))-(1/(B*M))-(1/(A*N)))

class kedalaman : 
    def __init__(self,a,b,m,n):
        self.a = a
        self.b = b
        self.m = m
        self.n = n
    def KW(a,b) : 
        return np.abs(a-b)
    def KWS(a,b,m,n):
        am = m-a
        bn = b-n
        mn = n-m 
        A = am
        N = mn/A
        return 0.5*(N+1)*A
    def KS(a,b) :
        return 0.5 * np.abs(a-b)
    def KG(a,b):
        return (0.2-0.3)*np.abs(a+b)
        
def R(dv,i):
    i = np.asarray(i, dtype=float)
    dv = np.asarray(dv, dtype=float)
    with np.errstate(divide='ignore', invalid='ignore'):
        R = dv / i
    R[~np.isfinite(R)] = np.nan
    return R
def rho_a(K,R):
    K = np.asarray(K, dtype=float)
    R = np.asarray(R, dtype=float)
    rho = K * R
    rho[~np.isfinite(rho)] = np.nan
    return rho

#method
if method == 'S':
    data["K"] = [Konfigurasi.S(a[i], b[i], m[i], n[i]) for i in range(len(a))]
elif method == 'W':
    data["K"] = [Konfigurasi.W(a[i],b[i]) for i in range(len(a))]
elif method == 'G':
    data["K"] = [Konfigurasi.G(a[i], m[i], b[i], n[i]) for i in range(len(a))]
elif method == 'WS':
    data["K"] = [Konfigurasi.WS(a[i], b[i], m[i], n[i]) for i in range(len(a))]
#kedalaman
if method == 'S':
    data["KD"] = [kedalaman.KS(a[i], b[i]) for i in range(len(a))]
elif method == 'W':
    data["KD"] = [kedalaman.KW(a[i],b[i]) for i in range(len(a))]
elif method == 'G':
    data["KD"] = [kedalaman.KG(a[i], b[i]) for i in range(len(a))]
elif method == 'WS':
    data["KD"] = [kedalaman.KWS(a[i], b[i], m[i], n[i]) for i in range(len(a))]


data["R"] = R(dv, i)
data["rho_a"] = rho_a(data["K"], data["R"])
values = np.log10(data["rho_a"].values)

x = np.array(data["A"])
y = np.array(data["B"])
z = np.array(data["rho_a"])
depths = np.array(data["KD"])

valid = ~np.isnan(z) & ~np.isnan(depths)
xp = np.asarray(x)[valid]
zp = np.asarray(depths)[valid]
rp = np.asarray(z)[valid]

if len(rp) >= 5 and len(np.unique(np.round(xp,8))) > 1 and len(np.unique(np.round(zp,8))) > 1:
    try:
        OK = OrdinaryKriging(xp, zp, rp, variogram_model='spherical', verbose=False, enable_plotting=False)
        grid_x = np.linspace(np.nanmin(xp), np.nanmax(xp), 200)
        grid_z = np.linspace(np.nanmin(zp), np.nanmax(zp), 100)
        z2_pred, ss2 = OK.execute('grid', grid_x, grid_z)
        plt.figure(figsize=(12,8), dpi=100)
        cf = plt.contourf(grid_x, grid_z, z2_pred, cmap='viridis', levels=50)
        plt.gca().invert_yaxis()
        plt.colorbar(cf, label='rho apparent (Ohm·m)')
        plt.xlabel('jarak elektroda (m)')
        plt.ylabel('Kedalaman (m)')
        plt.title('Penampang ERT')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        print('kriging gagal', e)
else:
    print('tambahin valid point woy')