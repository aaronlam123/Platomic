from PyQt5 import QtWidgets
from glaxis import GLAxis
from glview import *
import sys
import unittest
from unittest.mock import MagicMock
app = QtWidgets.QApplication(sys.argv)


class TestGlaxis(unittest.TestCase):
    def setUp(self):
        self.w = GLView()
        self.axis = GLAxis(self.w)
        self.axis.setSize(x=1, y=1, z=1)
        self.axis.add_tick_values(x=[0, 1, 2], y=[0, 1, 2], z=[0, 0.5, 1])
        self.w.addItem(self.axis)
        self.axis.add_labels = MagicMock()
        self.axis.setupGLState = MagicMock()

    def test_axis_add_labels(self):
        self.axis.add_labels()
        self.axis.add_labels.assert_called_once()

    def test_axis_paint(self):
        self.axis.paint()
        self.axis.setupGLState.assert_called_once()