from pyqtgraph.opengl import GLViewWidget
from OpenGL.GL import *
import pyqtgraph as pg
import numpy as np


class GLView3D(GLViewWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.multiplier = None

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
