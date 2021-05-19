import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import tkinter
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler

H = [[0, 1, 0, 0, 0, 1], [1, 0, 1, 0, 0, 0], [0, 1, 0, 1, 0, 0], [0, 0, 1, 0, 1, 0], [0, 0, 0, 1, 0, 1], [1, 0, 0, 0, 1, 0]]
H = np.array(H)
#print(H)

eigenvalues, eigenvectors = np.linalg.eig(H)
#print("Eigenvalues: %s " % eigenvalues)
#print("Eigenvectors:")
#print(eigenvectors)

transform = np.zeros((6,6))
for i in range(6):
  for j in range(6):
    transform[i][j] = eigenvectors[j][i]

H_diag = np.matmul(np.matmul(transform, H), np.linalg.inv(transform))


a = 0.25
offset = 0.05
hex_coords = [[2*a, 0], [a, a*math.sqrt(3)], [-a, a*math.sqrt(3)], [-2*a, 0], [-a, -a*math.sqrt(3)], [a, -a*math.sqrt(3)]]
hex_offset = [[2*a + offset, 0], [a + offset, a*math.sqrt(3)], [-a - offset, a*math.sqrt(3)], [-2*a - offset, 0], [-a - offset, -a*math.sqrt(3)], [a + offset, -a*math.sqrt(3)]]

hydrogen_distance = 1.6
center_z = 0
r = 0.1
alpha = 1.3
#fig = plt.figure(figsize=plt.figaspect(1.))
#ax = fig.add_subplot(projection='3d')

def draw_benzene():
    for i in range(6):  #plot carbon atoms
      u = np.linspace(0, 2 * np.pi, 6)
      v = np.linspace(0, np.pi, 6)
      x = r * np.outer(np.cos(u), np.sin(v)) + hex_coords[i][0]
      y = r * np.outer(np.sin(u), np.sin(v)) + hex_coords[i][1]
      z = r * np.outer(np.ones(np.size(u)), np.cos(v)) + center_z
      ax.plot_surface(x, y, z, color='grey')

      for each in range(6):
        u = np.linspace(0, 2 * np.pi, 6) #change wire mesh density
        v = np.linspace(0, np.pi, 6)
        radius = alpha * np.square(eigenvectors[i][j]) #radius of electron density
        x = radius * np.outer(np.cos(u), np.sin(v)) + hex_coords[i][0]
        y = radius * np.outer(np.sin(u), np.sin(v)) + hex_coords[i][1]
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v)) + center_z
        ax.plot_wireframe(x, y, z, color='red', linewidth=0.01) #plot wireframe
        ax.plot([hex_coords[i][0], hex_coords[i-1][0]],
                [hex_coords[i][1], hex_coords[i-1][1]],
                [0, 0], color='black') #plot carbon bonds

        x = r/1.42 * np.outer(np.cos(u), np.sin(v)) + hydrogen_distance * hex_coords[i][0]
        y = r/1.42 * np.outer(np.sin(u), np.sin(v)) + hydrogen_distance * hex_coords[i][1]
        z = r/1.42 * np.outer(np.ones(np.size(u)), np.cos(v)) + center_z
        ax.plot_surface(x, y, z, color='white')
        ax.plot([hex_coords[i][0], hydrogen_distance * hex_coords[i][0]],
                [hex_coords[i][1], hydrogen_distance * hex_coords[i][1]],
                [0, 0], color='black') #plot hydrogen bonds

    #ax.set_axis_off()
    #plt.title("Eigenvector %d" % (j + 1))
    #ax.set_xlim3d(-1.6, 1.6)
    #ax.set_ylim3d(-1.2, 1.2)
    #ax.set_zlim3d(-0.4, 0.4)
    #ax.view_init(50, 30) #change the (elevation, azimuthal angle)
    #plt.show()


root = tkinter.Tk()
root.config(background='white')
root.geometry("1000x700")

fig = Figure()
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.draw()

ax = fig.add_subplot(111, projection="3d")
draw_benzene() #adds benzene to ax

canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()

tkinter.mainloop()


"""
def on_key_press(event):
  print("you pressed {}".format(event.key))
  key_press_handler(event, canvas, toolbar)


canvas.mpl_connect("key_press_event", on_key_press)


def _quit():
  root.quit()  # stops mainloop
  root.destroy()  # this is necessary on Windows to prevent
  # Fatal Python Error: PyEval_RestoreThread: NULL tstate


#button = tkinter.Button(master=root, text="Quit", command=_quit)
#button.pack(side=tkinter.BOTTOM)
"""

