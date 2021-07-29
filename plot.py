from PyQt5 import QtGui
from scipy.spatial import distance
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import scipy.special as sp
import orbital
import pandas as pd
import matplotlib.pyplot as plt
from glaxis import GLAxis

RYDBERG = 13.605685


def colours(terminal):
    array = ['red', 'cyan', 'orange', 'blue', 'gray']
    colour = [(1, 0, 0, 0.5), (0, 1, 1, 0.5), (1, 0.5, 0, 0.5), (0, 0, 1, 0.5), (0.5, 0.5, 0.5, 0.5)]
    if isinstance(terminal, str):
        return array[int(terminal) - 1]
    else:
        return colour[terminal - 1]


def draw_atoms(atoms, widget, rows, cols):
    for i in range(len(atoms)):
        if atoms[i].get_mi() is None:
            md = gl.MeshData.sphere(rows=rows, cols=cols, radius=atoms[i].get_radius())
            mi = gl.GLMeshItem(meshdata=md, smooth=True, color=atoms[i].get_colour())
            mi.translate(*atoms[i].get_xyz())
            widget.addItem(mi)
            atoms[i].set_mi(mi)
        else:
            md = gl.MeshData.sphere(rows=rows, cols=cols, radius=atoms[i].get_radius())
            atoms[i].get_mi().setMeshData(meshdata=md)
            widget.addItem(atoms[i].get_mi())

def draw_selection(atoms, widget, rows, cols):
    for i in range(len(atoms)):
        md = gl.MeshData.sphere(rows=rows, cols=cols, radius=atoms[i].get_radius() + 0.02)
        if atoms[i].get_isSelectedTrans():
            mi = gl.GLMeshItem(meshdata=md, smooth=True, color=colours(atoms[i].get_isSelectedTrans()), drawEdges=False,
                               drawFaces=True)
            mi.translate(*atoms[i].get_xyz())
            mi.setGLOptions('translucent')
            widget.addItem(mi)
        if atoms[i].get_isSelectedCurrA():
            mi = gl.GLMeshItem(meshdata=md, smooth=True, edgeColor=(1, 0, 1, 1), drawEdges=True, drawFaces=False)
            mi.translate(*atoms[i].get_xyz())
            widget.addItem(mi)
        if atoms[i].get_isSelectedCurrB():
            tr = pg.Transform3D()
            tr.rotate(90 * 180 / np.pi, 0, 0, 1)
            mi = gl.GLMeshItem(meshdata=md, smooth=True, edgeColor=(0, 1, 0, 1), drawEdges=True, drawFaces=False)
            mi.setTransform(tr)
            mi.translate(*atoms[i].get_xyz())
            widget.addItem(mi)


def draw_bonds(atoms, widget, rows, cols, bond_radius, max_bond_length):
    for i in range(len(atoms)):
        for j in range(len(atoms)):
            if atoms[i].get_symbol() in atoms[j].get_bonding():
                continue
            if atoms[i].get_bondCount() <= 0:
                continue
            p2 = np.array(atoms[i].get_xyz())
            p1 = np.array(atoms[j].get_xyz())
            v = p2 - p1
            length = distance.euclidean(p1, p2)
            if (length / atoms[i].get_radius()) > max_bond_length or (length / atoms[j].get_radius()) > max_bond_length:
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
            atoms[j].decrement_bond_count()
    for i in range(len(atoms)):
        atoms[i].reset_bonds()


def draw_advOrbWf(atoms, widget, value, row, cols, scaler, theta, phi, r, g, b, a):
    for i in range(len(atoms)):
        if atoms[i].get_skipOrbital() == "True":
            continue
        for j in range(len(atoms[i].get_quantum_dict())):

            quantum_dict = atoms[i].get_quantum_dict()
            tr = pg.Transform3D()
            tr.rotate(theta * 180 / np.pi, 0, 0, 1)
            tr.rotate(phi * 180 / np.pi, 0, 1, 0)
            md = orbital.advanced_orbital(atoms[i].get_eigenvector(value)[j], quantum_dict[j][2], quantum_dict[j][1],
                                          row, cols,
                                          scaler)
            mi = gl.GLMeshItem(meshdata=md, smooth=True, edgeColor=(r, g, b, a), drawEdges=True, drawFaces=False)
            mi.setTransform(tr)
            mi.translate(*atoms[i].get_xyz())
            widget.addItem(mi)


def draw_advOrbHorz(atoms, widget, value, scaler, theta_, phi_, r, g, b, a):
    phi, theta = np.mgrid[0:np.pi:30j, 0:2 * np.pi:30j]
    for i in range(len(atoms)):
        for j in range(len(atoms[i].get_quantum_dict())):
            quantum_dict = atoms[i].get_quantum_dict()
            tr = pg.Transform3D()
            tr.rotate(theta_ * 180 / np.pi, 0, 0, 1)
            tr.rotate(phi_ * 180 / np.pi, 0, 1, 0)
            rad = scaler * \
                  atoms[i].get_eigenvector(value)[j] * \
                  np.abs(sp.sph_harm(quantum_dict[j][2], quantum_dict[j][1], theta, phi).real)
            x = rad * np.sin(phi) * np.cos(theta)
            y = rad * np.sin(phi) * np.sin(theta)
            z = rad * np.cos(phi)
            vertexes = np.dstack((x.flatten(), y.flatten()))
            vertexes = np.dstack((vertexes, z.flatten()))
            mi = gl.GLMeshItem(vertexes=vertexes, color=(r, g, b, a))
            mi.setTransform(tr)
            mi.translate(*atoms[i].get_xyz())
            widget.addItem(mi)


def draw_advOrbVert(atoms, widget, value, scaler, theta_, phi_, r, g, b, a):
    theta, phi = np.mgrid[0:2 * np.pi:30j,
                 0:np.pi:30j]  # swapping theta and phi here changes plotting to vert wireframe
    for i in range(len(atoms)):
        for j in range(len(atoms[i].get_quantum_dict())):
            quantum_dict = atoms[i].get_quantum_dict()
            tr = pg.Transform3D()
            tr.rotate(theta_ * 180 / np.pi, 0, 0, 1)
            tr.rotate(phi_ * 180 / np.pi, 0, 1, 0)
            rad = scaler * \
                  atoms[i].get_eigenvector(value)[j] * \
                  np.abs(sp.sph_harm(quantum_dict[j][2], quantum_dict[j][1], theta, phi).real)
            x = rad * np.sin(phi) * np.cos(theta)
            y = rad * np.sin(phi) * np.sin(theta)
            z = rad * np.cos(phi)
            vertexes = np.dstack((x.flatten(), y.flatten()))
            vertexes = np.dstack((vertexes, z.flatten()))
            mi = gl.GLMeshItem(vertexes=vertexes, color=(r, g, b, a))
            mi.setTransform(tr)
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
        mi = gl.GLMeshItem(meshdata=md, smooth=True, color=(r, g, b, a), drawEdges=False, drawFaces=True)
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
            md = orbital.advanced_orbital(atoms[i].get_eigenvector(value)[j], quantum_dict[j][2], quantum_dict[j][1],
                                          row, cols,
                                          scaler)
            mi = gl.GLMeshItem(meshdata=md, smooth=True, color=(r, g, b, a), drawEdges=False, drawFaces=True)
            mi.setTransform(tr)
            mi.translate(*atoms[i].get_xyz())
            mi.setGLOptions('translucent')
            widget.addItem(mi)


def transmission_graph(widget, input_file, index, offset=0):
    widget.clear()
    widget.setBackground('w')
    labelStyle = {'color': '#FFF', 'font-size': '12pt'}
    widget.setLabel("left", text="Transmission", **labelStyle)
    widget.setLabel("bottom", text="Energy", units="eV", **labelStyle)

    font = QtGui.QFont()
    font.setPixelSize(14)
    pen = pg.mkPen(width=3, color='k')
    widget.getAxis("bottom").setStyle(tickFont=font)
    widget.getAxis("left").setStyle(tickFont=font)
    widget.getAxis("bottom").setTextPen(pen)
    widget.getAxis("left").setTextPen(pen)
    widget.getAxis("bottom").setPen(pen)
    widget.getAxis("left").setPen(pen)

    widget.addItem(pg.InfiniteLine(pos=(0, 0), pen=pg.mkPen(width=3, color='r')))
    widget.getViewBox().suggestPadding = lambda *_: 0.0
    df = pd.read_csv(input_file, sep=",", quoting=3)
    if index == "All":
        for i in list(df):
            if i == "E(Ry)":
                continue
            widget.plot(df["E(Ry)"] * RYDBERG - offset, df[i], pen=pen)
    else:
        widget.plot(df["E(Ry)"] * RYDBERG - offset, df[index], pen=pen)


def current_graph(widget, x, y):
    widget.clear()
    widget.setBackground('w')
    labelStyle = {'color': '#FFF', 'font-size': '12pt'}
    widget.setLabel("left", text="Current", units="mA", **labelStyle)
    widget.setLabel("bottom", text="Bias", units="V", **labelStyle)

    font = QtGui.QFont()
    font.setPixelSize(14)
    pen = pg.mkPen(width=3, color='k')
    widget.getAxis("bottom").setStyle(tickFont=font)
    widget.getAxis("left").setStyle(tickFont=font)
    widget.getAxis("bottom").setTextPen(pen)
    widget.getAxis("left").setTextPen(pen)
    widget.getAxis("bottom").setPen(pen)
    widget.getAxis("left").setPen(pen)

    widget.getViewBox().suggestPadding = lambda *_: 0.0
    widget.plot(x, y, pen=pen)


def energy_gamma_trans_graph(widget, x, y, z):
    widget.clear()
    min_z = np.min(z)
    max_z = np.max(z)
    cmap = plt.get_cmap('jet')
    colour_map = cmap((z - min_z) / (max_z - min_z))
    surf = gl.GLSurfacePlotItem(x, y, z, colors=colour_map)
    surf.translate((np.max(x) - np.min(x)) / 2, 0, 0)
    widget.addItem(surf)

    axis = GLAxis(widget)
    axis.setSize(x=(np.max(x) - np.min(x)), y=(np.max(y) - np.min(y)), z=(np.max(z) - np.min(z)))
    axis.add_labels()
    axis.add_tick_values(x, y, z)
    widget.addItem(axis)
