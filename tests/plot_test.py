import unittest
from main import *

resolution = pyautogui.size()
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QtWidgets.QApplication(sys.argv)
default_input = input_file_setup("config/benzene.out", "config/attributes.txt", "config/benzene.wf")


class TestPlot(unittest.TestCase):
    def setUp(self):
        self.main = MainWindow(default_input, resolution.width)
        self.main.openGLWidget.clear()

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
