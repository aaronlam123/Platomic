from PyQt5 import QtWidgets
from PyQt5.Qt import QApplication

from atom import Atom
from glview import *
import pyqtgraph.opengl as gl
from OpenGL.GL import *
import os
import sys
import unittest
from unittest.mock import MagicMock
from pyqtgraph.opengl import GLViewWidget
from PyQt5.QtTest import QTest, QSignalSpy
from PyQt5.QtCore import Qt, QPoint

app = QtWidgets.QApplication(sys.argv)


class TestGlView(unittest.TestCase):
    def setUp(self):
        self.w = GLView()
        self.w.resize(800, 600)
        self.w.atoms = [Atom("C", 0, 0, 0, 1), Atom("H", 1, 1, 0, 2), Atom("H", 2, 2, 0, 3)]
        self.w.multiplier = 2
        self.w.size = 10
        self.w.colour = "Red"
        self.w.font = "Arial"
        md = gl.MeshData.sphere(rows=10, cols=20, radius=1)
        mi = gl.GLMeshItem(meshdata=md, smooth=True, color=(1, 1, 1, 1))
        mi.translate(0, 0, 0)
        self.w.addItem(mi)
        self.w.renderText = MagicMock()
        # QTest.mouseClick(self.w, Qt.LeftButton)
        # self.left_clicked_bool = False
        # self.w.left_clicked.connect(self.left_click_called)

    def left_click_called(self):
        print("value")

    def test_mousePressEvent(self):
        QTest.mouseClick(self.w, Qt.RightButton, pos=QPoint(0, 0))

    def test_itemsAt(self):
        print(self.w.itemsAt(region=(0, 0, 500, 500)))

    def test_paintGL(self):
        self.w.paintGL()
        self.w.renderText.assert_called_once()

    def test_readQImage(self):
        self.assertEqual(self.w.readQImage().width(), self.w.width() * self.w.multiplier)
        self.assertEqual(self.w.readQImage().height(), self.w.height() * self.w.multiplier)
