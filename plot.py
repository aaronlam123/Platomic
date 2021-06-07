from scipy.spatial import distance
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import scipy.special as sp
import custom

from Transmission.Transmission import get_energy_gamma_transmission_XYZ


""" Deprecated functions
def draw_atom(radius, position, widget, colour, wireframe=False):
    md = gl.MeshData.sphere(rows=10, cols=20, radius=radius)
    mi = gl.GLMeshItem(meshdata=md, smooth=True, color=colour, shader="balloon")
    if wireframe:
        mi = gl.GLMeshItem(meshdata=md, smooth=True, color=(0, 0, 0, 1), shader="balloon", drawEdges=True,
                           drawFaces=False)
    mi.translate(*position)
    widget.addItem(mi)


def draw_bond(p1, p2, widget, bond_radius=0.1):
    v = p2 - p1
    theta = np.arctan2(v[1], v[0])
    phi = np.arctan2(np.linalg.norm(v[:2]), v[2])
    tr = pg.Transform3D()
    tr.translate(*p1)
    tr.rotate(theta * 180 / np.pi, 0, 0, 1)
    tr.rotate(phi * 180 / np.pi, 0, 1, 0)
    md = gl.MeshData.cylinder(rows=10, cols=20, radius=[bond_radius, bond_radius], length=distance.euclidean(p1, p2))
    mi = gl.GLMeshItem(meshdata=md, smooth=True, color=(0.6, 0.6, 0.6, 0), shader="balloon", drawFaces=True)
    mi.setTransform(tr)
    widget.addItem(mi)
"""


def draw_atoms(atoms, widget, rows, cols):
    for i in range(len(atoms)):
        md = gl.MeshData.sphere(rows=rows, cols=cols, radius=atoms[i].get_radius())
        mi = gl.GLMeshItem(meshdata=md, smooth=True, color=atoms[i].get_colour())
        mi.translate(*atoms[i].get_xyz())
        widget.addItem(mi)


def draw_bonds(atoms, widget, rows, cols, bond_radius, max_bond_length):
    for i in range(len(atoms)):
        for j in range(len(atoms)):
            if atoms[i].get_symbol() in atoms[j].get_bonding():
                continue
            p2 = np.array(atoms[i].get_xyz())
            p1 = np.array(atoms[j].get_xyz())
            v = p2 - p1
            length = distance.euclidean(p1, p2)
            if length > max_bond_length:
                continue
            theta = np.arctan2(v[1], v[0])
            phi = np.arctan2(np.linalg.norm(v[:2]), v[2])
            tr = pg.Transform3D()
            tr.translate(*p1)
            tr.rotate(theta * 180 / np.pi, 0, 0, 1)
            tr.rotate(phi * 180 / np.pi, 0, 1, 0)
            md = gl.MeshData.cylinder(rows=rows, cols=cols, radius=[bond_radius, bond_radius], length=length)
            mi = gl.GLMeshItem(meshdata=md, smooth=True, color=(0.6, 0.6, 0.6, 1), drawFaces=True)
            mi.setTransform(tr)
            widget.addItem(mi)


def draw_advOrbWf(atoms, widget, value, row, cols, scaler, theta, phi, r, g, b, a):
    for i in range(len(atoms)):
        for j in range(len(atoms[i].get_quantum_dict())):
            quantum_dict = atoms[i].get_quantum_dict()
            tr = pg.Transform3D()
            tr.rotate(theta * 180 / np.pi, 0, 0, 1)
            tr.rotate(phi * 180 / np.pi, 0, 1, 0)
            md = custom.orbital(atoms[i].get_eigenvector(value)[j], quantum_dict[j][2], quantum_dict[j][1], row, cols, scaler)
            mi = gl.GLMeshItem(meshdata=md, smooth=True, edgeColor=(r, g, b, a), drawEdges=True, drawFaces=False)
            mi.setTransform(tr)
            mi.translate(*atoms[i].get_xyz())
            widget.addItem(mi)


def draw_advOrbHorz(atoms, widget, value, scaler, r, g, b, a):
    phi, theta = np.mgrid[0:np.pi:30j, 0:2*np.pi:30j]
    for i in range(len(atoms)):
        for j in range(len(atoms[i].get_quantum_dict())):
            quantum_dict = atoms[i].get_quantum_dict()
            rad = scaler * \
                atoms[i].get_eigenvector(value)[j] * \
                np.abs(sp.sph_harm(quantum_dict[j][2], quantum_dict[j][1], theta, phi).real)
            x = rad * np.sin(phi) * np.cos(theta)
            y = rad * np.sin(phi) * np.sin(theta)
            z = rad * np.cos(phi)
            vertexes = np.dstack((x.flatten(), y.flatten()))
            vertexes = np.dstack((vertexes, z.flatten()))
            mi = gl.GLMeshItem(vertexes=vertexes, color=(r, g, b, a))
            mi.translate(*atoms[i].get_xyz())
            widget.addItem(mi)


def draw_advOrbVert(atoms, widget, value, scaler, r, g, b, a):
    theta, phi = np.mgrid[0:2*np.pi:30j, 0:np.pi:30j] # swapping theta and phi here changes plotting to vert wireframe
    for i in range(len(atoms)):
        for j in range(len(atoms[i].get_quantum_dict())):
            quantum_dict = atoms[i].get_quantum_dict()
            rad = scaler * \
                atoms[i].get_eigenvector(value)[j] * \
                np.abs(sp.sph_harm(quantum_dict[j][2], quantum_dict[j][1], theta, phi).real)
            x = rad * np.sin(phi) * np.cos(theta)
            y = rad * np.sin(phi) * np.sin(theta)
            z = rad * np.cos(phi)
            vertexes = np.dstack((x.flatten(), y.flatten()))
            vertexes = np.dstack((vertexes, z.flatten()))
            mi = gl.GLMeshItem(vertexes=vertexes, color=(r, g, b, a))
            mi.translate(*atoms[i].get_xyz())
            widget.addItem(mi)


def draw_sphOrbWf(atoms, widget, mode, rows, cols, scaler, r, g, b, a):
    for i in range(len(atoms)):
        radius = np.sum(np.square(atoms[i].get_eigenvector(mode)))
        md = gl.MeshData.sphere(rows=rows, cols=cols, radius=radius * scaler)
        mi = gl.GLMeshItem(meshdata=md, smooth=True, edgeColor=(r, g, b, a), drawEdges=True, drawFaces=False)
        mi.translate(*atoms[i].get_xyz())
        widget.addItem(mi)


def draw_sphOrbFaces(atoms, widget, mode, rows, cols, scaler, r, g, b, a):
    for i in range(len(atoms)):
        radius = np.sum(np.square(atoms[i].get_eigenvector(mode)))
        md = gl.MeshData.sphere(rows=rows, cols=cols, radius=radius * scaler)
        mi = gl.GLMeshItem(meshdata=md, smooth=True, color=(r, g, b, a), drawEdges=False, drawFaces=True, shader='balloon')
        mi.translate(*atoms[i].get_xyz())
        mi.setGLOptions('translucent')
        widget.addItem(mi)


def draw_advOrbFaces(atoms, widget, value, row, cols, scaler, theta, phi, r, g, b, a):
    for i in range(len(atoms)):
        for j in range(len(atoms[i].get_quantum_dict())):
            quantum_dict = atoms[i].get_quantum_dict()
            tr = pg.Transform3D()
            tr.rotate(theta * 180 / np.pi, 0, 0, 1)
            tr.rotate(phi * 180 / np.pi, 0, 1, 0)
            md = custom.orbital(atoms[i].get_eigenvector(value)[j], quantum_dict[j][2], quantum_dict[j][1], row, cols, scaler)
            mi = gl.GLMeshItem(meshdata=md, smooth=True, color=(r, g, b, a), drawEdges=False, drawFaces=True)
            mi.setTransform(tr)
            mi.translate(*atoms[i].get_xyz())
            mi.setGLOptions('translucent')
            widget.addItem(mi)

