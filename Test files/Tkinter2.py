import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler


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


# fig = plt.figure(figsize=plt.figaspect(1.))
# ax = fig.add_subplot(projection='3d')

def draw_benzene():
    for i in range(6):  # plot carbon atoms
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = r * np.outer(np.cos(u), np.sin(v)) + hex_coords[i][0]
        y = r * np.outer(np.sin(u), np.sin(v)) + hex_coords[i][1]
        z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + center_z
        ax.plot_surface(x, y, z, color='grey')

        for each in range(6):
            u = np.linspace(0, 2 * np.pi, 10)  # change wire mesh density
            v = np.linspace(0, np.pi, 10)
            radius = alpha * np.square(eigenvectors[i][j])  # radius of electron density
            x = radius * np.outer(np.cos(u), np.sin(v)) + hex_coords[i][0]
            y = radius * np.outer(np.sin(u), np.sin(v)) + hex_coords[i][1]
            z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center_z
            ax.plot_wireframe(x, y, z, color='red', linewidth=0.01)  # plot wireframe
            ax.plot([hex_coords[i][0], hex_coords[i - 1][0]],
                    [hex_coords[i][1], hex_coords[i - 1][1]],
                    [0, 0], color='black')  # plot carbon bonds

            x = r / 1.42 * np.outer(np.cos(u), np.sin(v)) + hydrogen_distance * hex_coords[i][0]
            y = r / 1.42 * np.outer(np.sin(u), np.sin(v)) + hydrogen_distance * hex_coords[i][1]
            z = r / 1.42 * np.outer(np.ones(np.size(u)), np.cos(v)) + center_z
            ax.plot_surface(x, y, z, color='white')
            ax.plot([hex_coords[i][0], hydrogen_distance * hex_coords[i][0]],
                    [hex_coords[i][1], hydrogen_distance * hex_coords[i][1]],
                    [0, 0], color='black')  # plot hydrogen bonds

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

fig = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

ax = fig.add_subplot(111, projection="3d")
draw_benzene() #adds benzene to ax

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()


canvas.mpl_connect("key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

button = tkinter.Button(master=root, text="Quit", command=root.quit)

# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
button.pack(side=tkinter.BOTTOM)
toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

tkinter.mainloop()