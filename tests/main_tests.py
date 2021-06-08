import unittest
from unittest.mock import MagicMock
from PyQt5.QtCore import Qt

from main import *
from PyQt5.QtTest import QTest

resolution = pyautogui.size()
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QtWidgets.QApplication(sys.argv)
default_input = input_file_setup("config/benzene.out", "config/attributes.txt", "config/benzene.wf")


class TestMain(unittest.TestCase):
    def setUp(self):
        self.main = MainWindow(default_input, resolution.width)
        with open("benzene.in", "w") as f:
            pass
        with open("benzene_.in", "w") as f:
            pass
        with open("attributes.txt", "w") as f:
            pass
        self.main.writeToLogs = MagicMock()
        self.main.writeErrorToLogs = MagicMock()
        self.main.draw = MagicMock()
        self.main.openGLWidget.setBackgroundColor = MagicMock()
        self.main.draw_advOrbWf = MagicMock()
        self.main.draw_advOrbHorz = MagicMock()
        self.main.draw_advOrbVert = MagicMock()
        self.main.draw_sphOrbWf = MagicMock()
        self.main.draw_sphOrbFaces = MagicMock()
        self.main.draw_advOrbFaces = MagicMock()

        # self.main.toggleAtomsButton.setChecked(False)
        # self.main.advOrbWfCheckBox.setChecked(False)
        # self.main.advOrbHorzCheckBox.setChecked(False)
        # self.main.advOrbVertCheckBox.setChecked(False)
        # self.main.sphOrbWfCheckBox.setChecked(False)
        # self.main.sphOrbFacesCheckBox.setChecked(False)
        # self.main.advOrbFacesCheckBox.setChecked(False)

    def tearDown(self):
        os.remove("benzene.in")
        os.remove("benzene_.in")
        os.remove("attributes.txt")
        copy_file_from_main_config("config/attributes.txt")

    if os.name == 'nt':
        def test_onExecuteButtonClicked_on_windows(self):
            QTest.mouseClick(self.main.executeButton, Qt.LeftButton)
            self.main.writeErrorToLogs.assert_called_with("Plato back-end execution is not supported on Windows systems.")
    else:
        def test_onExecuteButtonClicked_with_no_input_file(self):
            QTest.mouseClick(self.main.executeButton, Qt.LeftButton)
            self.main.writeErrorToLogs.assert_called_with(
                "No Plato input file found, click generate before clicking execute.")
            unittest.TestCase.assertRaises(self, expected_exception=TypeError)

        def test_onExecuteButtonClicked_with_input_file(self):
            self.main.openFileLineEdit.setText("test_files/benzene.xyz")
            QTest.mouseClick(self.main.generateInputFileButton, Qt.LeftButton)
            QTest.mouseClick(self.main.executeButton, Qt.LeftButton)
            self.main.writeToLogs.assert_called()
            self.main.draw.assert_called_once()

    def test_onGenerateInputFileButtonClicked_and_file_exists(self):
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateInputFileButton, Qt.LeftButton)
        self.assertEqual(self.main.inputFilename, "benzene_")
        with open("test_files/correct.in") as correct:
            self.assertEqual(correct.read(), self.main.inputTextEdit.toPlainText())
        self.main.writeToLogs.assert_called_with("Input file benzene_.in generated successfully.", "green")

    def test_onGenerateInputFileButtonClicked_with_nonexistent_file(self):
        self.main.openFileLineEdit.setText("test_files/nonexistent.xyz")
        QTest.mouseClick(self.main.generateInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with("Error: No .xyz file selected to generate Plato input file.")
        unittest.TestCase.assertRaises(self, expected_exception=IOError)

    def test_onGenerateInputFileButtonClicked_with_nonexistent_default_input(self):
        os.remove("config/default.in")
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with(
            "Error: No default input file found, check that config/default.in exists.")
        unittest.TestCase.assertRaises(self, expected_exception=FileNotFoundError)
        copy_file_from_main_config("config/default.in")

    def test_onOpenFileButtonClicked(self):
        pass
        #QTest.mouseClick(self.main.openFileButton, Qt.LeftButton)
        #self.assertEqual(self.main.openFileLineEdit.text(), "C:/Users/Aaron Lam/Downloads/Platomic/tests/test_files/benzene.xyz")

    def test_onSwitchToInputFileTabButtonClicked(self):
        QTest.mouseClick(self.main.switchToInputFileTabButton, Qt.LeftButton)
        self.assertEqual(self.main.mainWindow.currentIndex(), self.main.mainWindow.indexOf(self.main.inputFileTab))

    def test_setAtomColSliderLabel(self):
        self.main.atomColSlider.setValue(40)
        self.assertIs(self.main.atomCol, 40)
        self.assertEqual(self.main.atomColSliderLabel.text(), "Columns: 40")
        self.main.draw.assert_called_once()

    def test_setAtomRowSliderLabel(self):
        self.main.atomRowSlider.setValue(20)
        self.assertIs(self.main.atomRow, 20)
        self.assertEqual(self.main.atomRowSliderLabel.text(), "Rows: 20")
        self.main.draw.assert_called_once()

    def test_setBondColSliderLabel(self):
        self.main.bondColSlider.setValue(15)
        self.assertIs(self.main.bondCol, 15)
        self.assertEqual(self.main.bondColSliderLabel.text(), "Columns: 15")
        self.main.draw.assert_called_once()

    def test_setBondRowSliderLabel(self):
        self.main.bondRowSlider.setValue(25)
        self.assertIs(self.main.bondRow, 25)
        self.assertEqual(self.main.bondRowSliderLabel.text(), "Rows: 25")
        self.main.draw.assert_called_once()

    def test_setBrightnessSliderLabel(self):
        self.main.brightnessSlider.setValue(100)
        self.assertEqual(self.main.backgroundColor, (100, 100, 100))
        self.assertEqual(self.main.brightnessSliderLabel.text(), "Brightness: 100")
        self.main.openGLWidget.setBackgroundColor.assert_called_with(self.main.backgroundColor)

    def test_setBondRadiusSliderLabel(self):
        self.main.bondRadiusSlider.setValue(20)
        self.assertEqual(self.main.bondRadius, 0.2)
        self.assertEqual(self.main.bondRadiusSliderLabel.text(), "Radius: 0.2")
        self.main.draw.assert_called_once()

    def test_setBondThresholdSliderLabel(self):
        self.main.bondThresholdSlider.setValue(40)
        self.assertEqual(self.main.bondThreshold, 4.0)
        self.assertEqual(self.main.bondThresholdSliderLabel.text(), "Length: 4.0")
        self.main.draw.assert_called_once()

    def test_onSwitchToAttrFileTabButtonClicked(self):
        QTest.mouseClick(self.main.switchToAttrFileTabButton, Qt.LeftButton)
        self.assertEqual(self.main.mainWindow.currentIndex(), self.main.mainWindow.indexOf(self.main.attributeFileTab))

    def test_draws_advOrbWf(self):
        pass
        # QTest.mousePress(self.main.advOrbWfCheckBox, Qt.LeftButton)
        # self.main.advOrbWfCheckBox.pressed()
        # QTest.mouseDClick(self.main.advOrbWfCheckBox, Qt.LeftButton)
        # self.main.draw()
        # self.main.draw_advOrbWf()

        # QTest.mouseClick(self.main.advOrbWfCheckBox, Qt.LeftButton)
        # self.main.draw.assert_called_once()
        # self.main.draw_advOrbWf.assert_called_once()

    def test_setOrbColSliderLabel(self):
        self.main.orbColSlider.setValue(60)
        self.assertIs(self.main.orbCol, 60)
        self.assertEqual(self.main.orbColSliderLabel.text(), "Columns: 60")
        self.main.draw.assert_called_once()

    def test_setOrbRowSliderLabel(self):
        self.main.orbRowSlider.setValue(40)
        self.assertIs(self.main.orbRow, 40)
        self.assertEqual(self.main.orbRowSliderLabel.text(), "Rows: 40")
        self.main.draw.assert_called_once()

    def test_setScalerSliderLabel(self):
        self.main.orbScalerSlider.setValue(10)
        self.assertIs(self.main.orbScaler, 10)
        self.assertEqual(self.main.orbScalerSliderLabel.text(), "Scaler: 10")
        self.main.draw.assert_called_once()

    def test_setThetaSliderLabel(self):
        self.main.thetaSlider.setValue(270)
        self.assertEqual(self.main.theta, math.radians(270))
        self.assertEqual(self.main.thetaSliderLabel.text(), "Theta: 270")
        self.main.draw.assert_called_once()

    def test_setPhiSliderLabel(self):
        self.main.phiSlider.setValue(120)
        self.assertEqual(self.main.phi, math.radians(120))
        self.assertEqual(self.main.phiSliderLabel.text(), "Phi: 120")
        self.main.draw.assert_called_once()

    def test_setColourRSliderLabel(self):
        self.main.colourRSlider.setValue(50)
        self.assertEqual(self.main.R, 0.5)
        self.assertEqual(self.main.colourRSliderLabel.text(), "R: 0.5")
        self.main.draw.assert_called_once()

    def test_setColourGSliderLabel(self):
        self.main.colourGSlider.setValue(60)
        self.assertEqual(self.main.G, 0.6)
        self.assertEqual(self.main.colourGSliderLabel.text(), "G: 0.6")
        self.main.draw.assert_called_once()

    def test_setColourBSliderLabel(self):
        self.main.colourBSlider.setValue(70)
        self.assertEqual(self.main.B, 0.7)
        self.assertEqual(self.main.colourBSliderLabel.text(), "B: 0.7")
        self.main.draw.assert_called_once()

    def test_setColourASliderLabel(self):
        self.main.colourASlider.setValue(80)
        self.assertEqual(self.main.A, 0.8)
        self.assertEqual(self.main.colourASliderLabel.text(), "A: 0.8")
        self.main.draw.assert_called_once()

    def test_setHorizontalSliderLabel(self):
        self.main.horizontalSlider.setValue(5)
        self.assertIs(self.main.mode, 5)
        self.assertEqual(self.main.horizontalSliderLabel.text(), "Mode: 6")
        self.main.draw.assert_called_once()

    def test_onResetViewButtonClicked(self):
        pass

    def test_onSaveImageButtonClicked(self):
        pass

    def test_onToggleAtomsButtonClicked(self):
        pass

    def test_onSaveInputFileButtonClicked(self):
        self.main.inputFilename = "benzene"
        self.main.inputTextEdit.setText("Checking input is saved.")
        QTest.mouseClick(self.main.saveInputFileButton, Qt.LeftButton)
        with open("benzene.in") as saved_input:
            self.assertEqual(saved_input.readlines(), ["Checking input is saved."])
        self.main.writeToLogs.assert_called_with("Input file benzene.in saved successfully.", "green")

    def test_onSaveAttributeFileButtonClicked(self):
        self.main.attributeTextEdit.setText("Checking attr input is saved.")
        QTest.mouseClick(self.main.saveAttributeFileButton, Qt.LeftButton)
        with open("config/attributes.txt") as saved_attr_input:
            self.assertEqual(saved_attr_input.readlines(), ["Checking attr input is saved."])
        self.main.writeToLogs.assert_called_with(
            "Attribute file attributes.txt modified successfully. Settings will be applied on next "
            "execution", "green")

    def test_writeToLogs(self):
        pass

    def test_writeErrorToLogs(self):
        pass


def copy_file_from_main_config(filename):
    with open("../" + filename, 'r') as source:
        with open(filename, 'w') as f:
            for line in source:
                f.write(line)


if __name__ == "__main__":
    unittest.main()
