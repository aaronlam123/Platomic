from pyqtgraph.Qt import QtCore, QtGui
from plot import draw_atom, draw_bond
import pyqtgraph.opengl as gl
import numpy as np
import sys
import math


H = [[0, 1, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0], [0, 1, 0, 1, 0, 0], [0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, 1],
     [1, 0, 0, 0, 1, 0]]
H = np.array(H)
eigenvalues, eigenvectors = np.linalg.eig(H)

a = 0.25
offset = 0.05
hex_coords = [[2 * a, 0], [a, a * math.sqrt(3)], [-a, a * math.sqrt(3)], [-2 * a, 0], [-a, -a * math.sqrt(3)],
              [a, -a * math.sqrt(3)]]

h_distance = 1.6
center_z = 0
r = 0.1
alpha = 1.3
bond_radius = 0.02


class Visualizer(object):
    def __init__(self):
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 3
        self.w.setWindowTitle('pyqtgraph example: GLLinePlotItem')
        self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()

        # create the background grids
        gx = gl.GLGridItem()
        gx.rotate(90, 0, 1, 0)
        gx.translate(-10, 0, 0)
        self.w.addItem(gx)
        gy = gl.GLGridItem()
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -10, 0)
        self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.translate(0, 0, -10)
        self.w.addItem(gz)


        for i in range(6):
            # Plot carbon atoms
            draw_atom(r, hex_coords[i][0], hex_coords[i][1], 0, self.w)

            # Plot hydrogen atoms
            draw_atom(r/1.42, h_distance * hex_coords[i][0], h_distance * hex_coords[i][1], 0, self.w, (1, 1, 1, 1))

            # Plot orbitals
            radius = alpha * np.square(eigenvectors[i][5])
            draw_atom(radius, hex_coords[i][0], hex_coords[i][1], 0, self.w, wireframe=True)

            # Plot C-C bonds
            point1 = np.array([hex_coords[i][0], hex_coords[i][1], 0])
            point2 = np.array([hex_coords[i - 1][0], hex_coords[i - 1][1], 0])
            draw_bond(bond_radius, point1, point2, self.w)

            # Plot C-H bonds
            point3 = np.array([hex_coords[i][0], hex_coords[i][1], 0])
            point4 = np.array([h_distance * hex_coords[i][0], h_distance * hex_coords[i][1], 0])
            draw_bond(bond_radius, point3, point4, self.w)


    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()


if __name__ == '__main__':
    v = Visualizer()
    v.start()