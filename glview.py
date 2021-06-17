from PyQt5 import QtGui
from pyqtgraph.opengl import GLViewWidget
from PyQt5.QtGui import QColor
from OpenGL.GL import *
import pyqtgraph as pg
import numpy as np


class GLView(GLViewWidget):
    left_clicked = pg.QtCore.pyqtSignal()
    right_clicked = pg.QtCore.pyqtSignal()
    middle_clicked = pg.QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.multiplier = None
        self.atoms = None
        self.index = True
        self.symbol = None
        self.position = None
        self.radius = None
        self.font = None
        self.size = None
        self.offset = None
        self.colour = None

    def mousePressEvent(self, ev):
        self.mousePos = ev.pos()
        items = self.itemsAt((ev.x(), ev.y(), 1, 1))

        if self.atoms is not None:
            if ev.button() == 1 or ev.button() == 2 or ev.button() == 4:
                for i in range(len(self.atoms) - 1, -1, -1):
                    if self.atoms[i].get_mi() in items:
                        if ev.button() == 1:
                            if self.atoms[i].get_isSelectedTrans():
                                self.atoms[i].set_isSelectedTrans(False)
                            else:
                                self.atoms[i].set_isSelectedTrans(True)
                            self.left_clicked.emit()
                            break

                        if ev.button() == 2:
                            if self.atoms[i].get_isSelectedCurrA():
                                self.atoms[i].set_isSelectedCurrA(False)
                            else:
                                self.atoms[i].set_isSelectedCurrA(True)
                            self.middle_clicked.emit()
                            break

                        if ev.button() == 4:
                            if self.atoms[i].get_isSelectedCurrB():
                                self.atoms[i].set_isSelectedCurrB(False)
                            else:
                                self.atoms[i].set_isSelectedCurrB(True)
                            self.right_clicked.emit()
                            break

    def itemsAt(self, region=None):
        """
        Return a list of the items displayed in the region (x, y, w, h)
        relative to the widget.
        """
        region = (region[0] * self.multiplier, (self.height() - (region[1] + region[3])) * self.multiplier,
                  region[2] * self.multiplier, region[3] * self.multiplier)

        # buf = np.zeros(100000, dtype=np.uint)
        buf = glSelectBuffer(100000)
        try:
            glRenderMode(GL_SELECT)
            glInitNames()
            glPushName(0)
            self._itemNames = {}
            self.paintGL(region=region, useItemNames=True)

        finally:
            hits = glRenderMode(GL_RENDER)

        items = [(h.near, h.names[0]) for h in hits]
        items.sort(key=lambda i: i[0])
        return [self._itemNames[i[1]] for i in items]

    def paintGL(self, *args, **kwds):
        # Call parent
        GLViewWidget.paintGL(self, *args, **kwds)

        font = QtGui.QFont()
        font.setFamily(self.font)
        font.setPixelSize(self.size)
        self.qglColor(QColor(self.colour))
        offset = 0.5

        if self.atoms is not None:
            for i in range(len(self.atoms)):
                xyz = np.array(self.atoms[i].get_xyz())
                if self.index:
                    self.renderText(xyz[0], xyz[1], xyz[2], str(self.atoms[i].get_index()), font)
                    xyz[self.offset] = xyz[self.offset] - offset
                if self.symbol:
                    self.renderText(xyz[0], xyz[1], xyz[2], str(self.atoms[i].get_symbol()), font)
                    xyz[self.offset] = xyz[self.offset] - offset
                if self.position:
                    self.renderText(xyz[0], xyz[1], xyz[2], str(self.atoms[i].get_xyz()), font)
                    xyz[self.offset] = xyz[self.offset] - offset
                if self.radius:
                    self.renderText(xyz[0], xyz[1], xyz[2], str(self.atoms[i].get_radius()), font)

        # self.renderText(0, 0, 0, '(0, 0, 0) CENTER')
        # self.renderText(1, 0, 0, '(1, 0, 0) RIGHT')
        # self.renderText(-1, 0, 0, '(-1, 0, 0) LEFT')
        # self.renderText(0, 1, 0, '(0, 1, 0) DOWN')
        # self.renderText(0, -1, 0, '(0, -1, 0) TOP')
        # self.renderText(-4.07550, -2.35299, 0.0000, 'Hydrogen')

    def readQImage(self):
        w = self.width() * self.multiplier
        h = self.height() * self.multiplier
        self.repaint()
        pixels = np.empty((h, w, 4), dtype=np.ubyte)
        pixels[:] = 128
        pixels[..., 0] = 50
        pixels[..., 3] = 255

        glReadPixels(0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE, pixels)

        # swap B,R channels for Qt
        tmp = pixels[..., 0].copy()
        pixels[..., 0] = pixels[..., 2]
        pixels[..., 2] = tmp
        pixels = pixels[::-1]  # flip vertical

        img = pg.functions.makeQImage(pixels, transpose=False)
        return img
