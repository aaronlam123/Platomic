import numpy as np
import scipy.special as sp
import pyqtgraph.opengl as gl

# Adapted from https://pyqtgraph.readthedocs.io/en/latest/_modules/pyqtgraph/opengl/MeshData.html
def orbital(eig_val, m, l, rows, cols, scaler):
    verts = np.empty((rows + 1, cols, 3), dtype=float)

    phi = (np.arange(rows + 1) * np.pi / rows).reshape(rows + 1, 1)
    th = ((np.arange(cols) * 2 * np.pi / cols).reshape(1, cols))
    radius = scaler * eig_val * np.abs(sp.sph_harm(m, l, th, phi).real)

    # compute vertexes
    s = radius * np.sin(phi)
    verts[..., 2] = radius * np.cos(phi)
    verts[..., 0] = s * np.cos(th)
    verts[..., 1] = s * np.sin(th)
    verts = verts.reshape((rows + 1) * cols, 3)

    # compute faces
    faces = np.empty((rows * cols * 2, 3), dtype=np.uint)
    rowtemplate1 = ((np.arange(cols).reshape(cols, 1) + np.array([[0, 1, 0]])) % cols) + np.array([[0, 0, cols]])
    rowtemplate2 = ((np.arange(cols).reshape(cols, 1) + np.array([[0, 1, 1]])) % cols) + np.array([[cols, 0, cols]])
    for row in range(rows):
        start = row * cols * 2
        faces[start:start + cols] = rowtemplate1 + row * cols
        faces[start + cols:start + (cols * 2)] = rowtemplate2 + row * cols

    return gl.MeshData(vertexes=verts, faces=faces)