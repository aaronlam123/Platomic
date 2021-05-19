import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
# matplotlib inline
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import scipy as sci
import scipy.special as sp
from matplotlib import cm, colors

m, l = input("Enter m order and l order: ").split()
m = int(m)
l = int(l)
print(m, l)
phi, theta = np.mgrid[0:2 * np.pi:200j, 0:np.pi:100j]

if m == 0:
    R = np.abs(sp.sph_harm(m, l, phi, theta))
if m == 1 and l == 2:
    m1 = 2
    l1 = 3
    R = np.abs(sp.sph_harm(m1, l1, phi, theta).real)
if m == 2 and l == 3:
    m1 = 4
    l1 = 5
    R = np.abs(sp.sph_harm(m1, l1, phi, theta).real)
if m == l and m != 0:
    m1 = 2 * m
    l1 = 2 * l
    R = sp.sph_harm(m1, l1, phi, theta).real
if m == 1 and l == 3:
    m1 = 2
    l1 = 4
    R = sp.sph_harm(m1, l1, phi, theta).real

x = R * np.sin(theta) * np.cos(phi)
y = R * np.sin(theta) * np.sin(phi)
z = R * np.cos(theta)
N = R / R.max()
m = str(m)
fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=cm.jet(N))
ax.set_title('$|m={} , l= {}|$'.format(m, l), fontsize=20)
m = cm.ScalarMappable(cmap=cm.jet)
m.set_array(R)
fig.colorbar(m, shrink=0.8)
plt.show()