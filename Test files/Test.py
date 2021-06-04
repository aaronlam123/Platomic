import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import scipy.special as sp
from custom import orbital

np.os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "2"
app = QtGui.QApplication([])
app.setAttribute(pg.QtCore.Qt.AA_EnableHighDpiScaling)

w = gl.GLViewWidget()
w.show()
w.setWindowTitle('pyqtgraph example: GLMeshItem')
w.setCameraPosition(distance=5)

g = gl.GLGridItem()
g.scale(2, 2, 1)
w.addItem(g)

phi, theta = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j]
#theta=np.arange(0, np.pi, 30j)
l = 3
m = 2

R = np.abs(sp.sph_harm(m, l, phi, theta).real)
x = R * np.sin(theta) * np.cos(phi)
y = R * np.sin(theta) * np.sin(phi)
z = R * np.cos(theta)
x = x.flatten()
y = y.flatten()
z = z.flatten()
c = np.dstack((x, y))
c = np.dstack((c, z))

#md = gl.MeshData(vertexes=c)
md = orbital(0.1, 2, 3, 30, 30)

m1 = gl.GLMeshItem(meshdata=md, smooth=True, color=(0.5, 0.5, 0.5, 1), drawFaces=True)
w.addItem(m1)


if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()