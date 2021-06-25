from PyQt5 import QtWidgets
import sys
import unittest
from glview3D import GLView3D


app = QtWidgets.QApplication(sys.argv)


class TestGlView3D(unittest.TestCase):
    def setUp(self):
        self.w = GLView3D()

    def test_readQImage(self):
        self.assertEqual(self.w.readQImage().width(), self.w.width() * self.w.multiplier)
        self.assertEqual(self.w.readQImage().height(), self.w.height() * self.w.multiplier)
