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
        self.w.atoms = [Atom("C", 0, 0, 0, 1, 0.5), Atom("H", 1, 1, 0, 2, 0.5), Atom("H", 2, 2, 0, 3, 0.5)]
        self.w.multiplier = 2
        self.w.size = 10
        self.w.colour = "Red"
        self.w.font = "Arial"
        md = gl.MeshData.sphere(rows=10, cols=20, radius=5)
        mi = gl.GLMeshItem(meshdata=md, smooth=True, color=(1, 1, 1, 1))
        mi.translate(0, 0, 0)
        self.w.addItem(mi)
        self.w.atoms[0].set_mi(mi)
        self.w.terminal = 1

        self.w.renderText = MagicMock()
        self.left_clicked_signal = MagicMock()
        self.right_clicked_signal = MagicMock()
        self.middle_clicked_signal = MagicMock()
        self.w.left_clicked.connect(self.left_clicked_signal)
        self.w.right_clicked.connect(self.right_clicked_signal)
        self.w.middle_clicked.connect(self.middle_clicked_signal)

    def left_clicked_signal(self):
        pass

    def right_clicked_signal(self):
        pass

    def middle_clicked_signal(self):
        pass

    def test_mousePressEvent_left_select(self):
        QTest.mouseClick(self.w, Qt.LeftButton, pos=QPoint(200, 600))
        self.assertIs(self.w.atoms[0].get_isSelectedTrans(), 1)
        self.left_clicked_signal.assert_called_once()

    def test_mousePressEvent_left_deselect(self):
        QTest.mouseClick(self.w, Qt.LeftButton, pos=QPoint(200, 600))
        QTest.mouseClick(self.w, Qt.LeftButton, pos=QPoint(200, 600))
        self.assertIs(self.w.atoms[0].get_isSelectedTrans(), 0)
        self.assertEqual(self.left_clicked_signal.call_count, 2)

    def test_mousePressEvent_right_select(self):
        QTest.mouseClick(self.w, Qt.RightButton, pos=QPoint(200, 600))
        self.assertTrue(self.w.atoms[0].get_isSelectedCurrA())
        self.right_clicked_signal.assert_called_once()

    def test_mousePressEvent_right_deselect(self):
        QTest.mouseClick(self.w, Qt.RightButton, pos=QPoint(200, 600))
        QTest.mouseClick(self.w, Qt.RightButton, pos=QPoint(200, 600))
        self.assertFalse(self.w.atoms[0].get_isSelectedCurrA())
        self.assertEqual(self.right_clicked_signal.call_count, 2)

    def test_mousePressEvent_middle_select(self):
        QTest.mouseClick(self.w, Qt.MiddleButton, pos=QPoint(200, 600))
        self.assertTrue(self.w.atoms[0].get_isSelectedCurrB())
        self.middle_clicked_signal.assert_called_once()

    def test_mousePressEvent_middle_deselect(self):
        QTest.mouseClick(self.w, Qt.MiddleButton, pos=QPoint(200, 600))
        QTest.mouseClick(self.w, Qt.MiddleButton, pos=QPoint(200, 600))
        self.assertFalse(self.w.atoms[0].get_isSelectedCurrB())
        self.assertEqual(self.middle_clicked_signal.call_count, 2)

    def test_itemsAt(self):
        self.assertEqual(len(self.w.itemsAt(region=(0, 0, 500, 500))), 1)

    def test_paintGL_index(self):
        self.w.paintGL()
        self.assertEqual(self.w.renderText.call_count, 3)

    def test_paintGL_index_disable(self):
        self.w.index = False
        self.w.paintGL()
        self.assertEqual(self.w.renderText.call_count, 0)

    def test_paintGL_symbol(self):
        self.w.symbol = True
        self.w.paintGL()
        self.assertEqual(self.w.renderText.call_count, 6)

    def test_paintGL_position(self):
        self.w.position = True
        self.w.paintGL()
        self.assertEqual(self.w.renderText.call_count, 6)

    def test_paintGL_radius(self):
        self.w.radius = True
        self.w.paintGL()
        self.assertEqual(self.w.renderText.call_count, 6)

    def test_readQImage(self):
        self.assertEqual(self.w.readQImage().width(), self.w.width() * self.w.multiplier)
        self.assertEqual(self.w.readQImage().height(), self.w.height() * self.w.multiplier)
