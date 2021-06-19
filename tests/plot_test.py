import unittest
from unittest.mock import MagicMock
from main import *

resolution = pyautogui.size()
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QtWidgets.QApplication(sys.argv)
default_input = input_file_setup("config/benzene.out", "config/attributes.txt", "config/benzene.wf")


class TestPlot(unittest.TestCase):
    def setUp(self):
        self.main = MainWindow(resolution.width, default_input)
        self.main.openGLWidget.clear()
        self.main.graphWidget2.plot = MagicMock()
        self.main.graphWidget2.clear = MagicMock()

    def test_draw_atoms(self):
        draw_atoms(self.main.atoms, self.main.openGLWidget, self.main.atomRow, self.main.atomCol)
        self.assertIs(12, len(self.main.openGLWidget.itemsAt(region=(-121, -398, 1133, 771))))

    def test_draw_bonds(self):
        draw_bonds(self.main.atoms, self.main.openGLWidget, self.main.bondRow, self.main.bondCol, self.main.bondRadius,
                   self.main.bondThreshold)
        self.assertIs(36, len(self.main.openGLWidget.itemsAt(region=(-121, -398, 1133, 771))))

    def test_draw_advOrbWf(self):
        draw_advOrbWf(self.main.atoms, self.main.openGLWidget, self.main.mode, self.main.orbRow, self.main.orbCol,
                      self.main.orbScaler, self.main.theta, self.main.phi, self.main.R, self.main.G, self.main.B,
                      self.main.A)
        self.assertIs(30, len(self.main.openGLWidget.itemsAt(region=(-121, -398, 1133, 771))))

    def test_draw_advOrbHorz(self):
        draw_advOrbHorz(self.main.atoms, self.main.openGLWidget, self.main.mode,
                        self.main.orbScaler, self.main.R, self.main.G, self.main.B,
                        self.main.A)
        self.assertIs(30, len(self.main.openGLWidget.itemsAt(region=(-121, -398, 1133, 771))))

    def test_draw_advOrbVert(self):
        draw_advOrbVert(self.main.atoms, self.main.openGLWidget, self.main.mode,
                        self.main.orbScaler, self.main.R, self.main.G, self.main.B,
                        self.main.A)
        self.assertIs(30, len(self.main.openGLWidget.itemsAt(region=(-121, -398, 1133, 771))))

    def test_draw_draw_sphOrbWf(self):
        draw_sphOrbWf(self.main.atoms, self.main.openGLWidget, self.main.mode, self.main.orbRow, self.main.orbCol,
                      self.main.orbScaler, self.main.R, self.main.G, self.main.B, self.main.A)
        self.assertIs(12, len(self.main.openGLWidget.itemsAt(region=(-121, -398, 1133, 771))))

    def test_draw_sphOrbFaces(self):
        draw_sphOrbFaces(self.main.atoms, self.main.openGLWidget, self.main.mode, self.main.orbRow, self.main.orbCol,
                         self.main.orbScaler, self.main.R, self.main.G, self.main.B, self.main.A)
        self.assertIs(12, len(self.main.openGLWidget.itemsAt(region=(-121, -398, 1133, 771))))

    def test_draw_advOrbFaces(self):
        draw_advOrbFaces(self.main.atoms, self.main.openGLWidget, self.main.mode, self.main.orbRow, self.main.orbCol,
                         self.main.orbScaler, self.main.theta, self.main.phi, self.main.R, self.main.G, self.main.B,
                         self.main.A)
        self.assertIs(30, len(self.main.openGLWidget.itemsAt(region=(-121, -398, 1133, 771))))

    def test_draw_selection(self):
        self.main.atoms[0].set_isSelectedTrans(True)
        self.main.atoms[0].set_isSelectedCurrA(True)
        self.main.atoms[0].set_isSelectedCurrB(True)
        draw_selection(self.main.atoms, self.main.openGLWidget, 20, 20)
        self.assertIs(3, len(self.main.openGLWidget.itemsAt(region=(-121, -398, 1133, 771))))

    def test_transmission_graph_all(self):
        transmission_graph(self.main.graphWidget2, "test_files/test_trans_output.csv", "All")
        self.assertEqual(self.main.graphWidget2.plot.call_count, 6)
        self.main.graphWidget2.clear.assert_called_once()

    def test_transmission_graph_singular(self):
        transmission_graph(self.main.graphWidget2, "test_files/test_trans_output.csv", " 1 - 2")
        self.main.graphWidget2.plot.assert_called_once()
        self.main.graphWidget2.clear.assert_called_once()

    def test_current_graph(self):
        current_graph(self.main.graphWidget2, [1, 2, 3], [2, 3, 4])
        self.main.graphWidget2.plot.assert_called_once()
        self.main.graphWidget2.clear.assert_called_once()
