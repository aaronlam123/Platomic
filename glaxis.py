from PyQt5.QtGui import QColor
import pyqtgraph.opengl as gl
import OpenGL.GL as opengl
import numpy as np


class Label(gl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self, x, y, z, text):
        gl.GLGraphicsItem.GLGraphicsItem.__init__(self)
        self.x = x
        self.y = y
        self.z = z
        self.text = text

    def setGLViewWidget(self, GLViewWidget):
        self.GLViewWidget = GLViewWidget

    def paint(self):
        self.GLViewWidget.qglColor(QColor("white"))
        self.GLViewWidget.renderText(self.x, self.y, self.z, self.text)


class GLAxis(gl.GLAxisItem):
    def __init__(self, parent):
        gl.GLAxisItem.__init__(self)
        self.parent = parent

    def add_labels(self):
        x, y, z = self.size()
        self.xLabel = Label(x=x / 2, y=-0.4, z=-0.4, text="Energy (Ry)")
        self.xLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.xLabel)

        self.yLabel = Label(x=-0.4, y=y / 2, z=-0.4, text="Gamma")
        self.yLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.yLabel)

        self.zLabel = Label(x=-0.4, y=-0.4, z=z / 2, text="Transmission")
        self.zLabel.setGLViewWidget(self.parent)
        self.parent.addItem(self.zLabel)

    def add_tick_values(self, x, y, z):
        x_ticks = np.linspace(0, (np.max(x) - np.min(x)), 5)
        x_val = np.linspace(np.min(x), np.max(x), 5)
        y_ticks = np.linspace(np.min(y), np.max(y), 5)
        y_val = np.linspace(np.min(y), np.max(y), 5)
        z_ticks = np.linspace(0, 1, 5)
        # X label
        for i, tick in enumerate(x_ticks):
            val = Label(x=x_ticks[i], y=-0.2, z=-0.2, text=str(round(x_val[i], 1)))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)
        # Y label
        for i, tick in enumerate(y_ticks):
            val = Label(x=-0.2, y=y_ticks[i], z=-0.2, text=str(round(y_val[i], 1)))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)
        # Z label
        for i, tick in enumerate(z_ticks):
            val = Label(x=-0.2, y=-0.2, z=z_ticks[i], text=str(tick))
            val.setGLViewWidget(self.parent)
            self.parent.addItem(val)

    def paint(self):
        self.setupGLState()
        if self.antialias:
            opengl.glEnable(opengl.GL_LINE_SMOOTH)
            opengl.glHint(opengl.GL_LINE_SMOOTH_HINT, opengl.GL_NICEST)
        opengl.glBegin(opengl.GL_LINES)

        x, y, z = self.size()
        x_ticks = np.linspace(0, x, 5)
        y_ticks = np.linspace(0, y, 5)
        z_ticks = np.linspace(0, z, 5)

        # x-axis
        opengl.glColor4f(1, 1, 1, 1)
        opengl.glVertex3f(0, 0, 0)
        opengl.glVertex3f(x, 0, 0)
        for tick in x_ticks:
            opengl.glVertex3f(tick, 0, 0)
            opengl.glVertex3f(tick, -0.05, 0)

        # y-axis
        opengl.glColor4f(1, 1, 1, 1)
        opengl.glVertex3f(0, 0, 0)
        opengl.glVertex3f(0, y, 0)
        for tick in y_ticks:
            opengl.glVertex3f(0, tick, 0)
            opengl.glVertex3f(-0.05, tick, 0)

        # z-axis
        opengl.glColor4f(1, 1, 1, 1)
        opengl.glVertex3f(0, 0, 0)
        opengl.glVertex3f(0, 0, z)
        for tick in z_ticks:
            opengl.glVertex3f(0, 0, tick)
            opengl.glVertex3f(0.05, 0, tick)
            opengl.glVertex3f(0, 0, tick)
            opengl.glVertex3f(0, 0.05, tick)
        opengl.glEnd()
