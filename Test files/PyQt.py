from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import math



H = [[0, 1, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0], [0, 1, 0, 1, 0, 0], [0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, 1],
     [1, 0, 0, 0, 1, 0]]
H = np.array(H)
# print(H)

eigenvalues, eigenvectors = np.linalg.eig(H)
# print("Eigenvalues: %s " % eigenvalues)
# print("Eigenvectors:")
# print(eigenvectors)

transform = np.zeros((6, 6))
for i in range(6):
    for j in range(6):
        transform[i][j] = eigenvectors[j][i]

H_diag = np.matmul(np.matmul(transform, H), np.linalg.inv(transform))

a = 0.25
offset = 0.05
hex_coords = [[2 * a, 0], [a, a * math.sqrt(3)], [-a, a * math.sqrt(3)], [-2 * a, 0], [-a, -a * math.sqrt(3)],
              [a, -a * math.sqrt(3)]]
hex_offset = [[2 * a + offset, 0], [a + offset, a * math.sqrt(3)], [-a - offset, a * math.sqrt(3)],
              [-2 * a - offset, 0], [-a - offset, -a * math.sqrt(3)], [a + offset, -a * math.sqrt(3)]]

hydrogen_distance = 1.6
center_z = 0
r = 0.1
alpha = 1.3



class Widget(QtWidgets.QWidget): #or use QtWidgets.QOpenGLWidget
    def __init__(self):
        super().__init__()
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.canvas)

        for i in range(6):  # plot carbon atoms
            u = np.linspace(0, 2 * np.pi, 6)
            v = np.linspace(0, np.pi, 6)
            x = r * np.outer(np.cos(u), np.sin(v)) + hex_coords[i][0]
            y = r * np.outer(np.sin(u), np.sin(v)) + hex_coords[i][1]
            z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + center_z
            self.axes.plot_surface(x, y, z, color='grey')

            for each in range(6):
                u = np.linspace(0, 2 * np.pi, 6)  # change wire mesh density
                v = np.linspace(0, np.pi, 6)
                radius = alpha * np.square(eigenvectors[i][j])  # radius of electron density
                x = radius * np.outer(np.cos(u), np.sin(v)) + hex_coords[i][0]
                y = radius * np.outer(np.sin(u), np.sin(v)) + hex_coords[i][1]
                z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center_z
                self.axes.plot_wireframe(x, y, z, color='red', linewidth=0.1)  # plot wireframe
                self.axes.plot([hex_coords[i][0], hex_coords[i - 1][0]],
                               [hex_coords[i][1], hex_coords[i - 1][1]],
                               [0, 0], color='black')  # plot carbon bonds

                x = r / 1.42 * np.outer(np.cos(u), np.sin(v)) + hydrogen_distance * hex_coords[i][0]
                y = r / 1.42 * np.outer(np.sin(u), np.sin(v)) + hydrogen_distance * hex_coords[i][1]
                z = r / 1.42 * np.outer(np.ones(np.size(u)), np.cos(v)) + center_z
                self.axes.plot_surface(x, y, z, color='white')
                self.axes.plot([hex_coords[i][0], hydrogen_distance * hex_coords[i][0]],
                               [hex_coords[i][1], hydrogen_distance * hex_coords[i][1]],
                               [0, 0], color='black')  # plot hydrogen bonds

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    win = Widget()
    win.show()
    app.exec()


