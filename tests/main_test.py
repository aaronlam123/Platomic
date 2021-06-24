import filecmp
import unittest
from unittest.mock import MagicMock
from PyQt5.QtCore import Qt, QPoint
from main import *
from PyQt5.QtTest import QTest

resolution = pyautogui.size()
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QtWidgets.QApplication(sys.argv)
default_input = input_file_setup("config/benzene.out", "config/attributes.txt", "config/benzene.wf")


class TestMain(unittest.TestCase):
    def setUp(self):
        self.main = MainWindow(resolution.width, default_input)
        with open("attributes.txt", "w") as f:
            pass
        self.main.writeToLogs = MagicMock()
        self.main.writeErrorToLogs = MagicMock()
        self.main.draw = MagicMock()
        self.main.openGLWidget.reset = MagicMock()
        self.main.openGLWidget.setBackgroundColor = MagicMock()
        self.main.openGLWidget.renderText = MagicMock()
        self.main.openGLWidget.update = MagicMock()
        self.main.graphComboBox.clear = MagicMock()
        self.main.graphComboBox.addItems = MagicMock()
        self.main.consoleLog.setTextColor = MagicMock()
        self.main.fullConsoleLog.setTextColor = MagicMock()
        self.main.consoleLog.append = MagicMock()
        self.main.fullConsoleLog.apend = MagicMock()
        self.addCleanup(cleanUp)
        self.doCleanups()

    if os.name != 'nt':
        def test_execute(self):
            pass

        def test_onExecuteButtonClicked_with_no_input_file(self):
            QTest.mouseClick(self.main.executeButton, Qt.LeftButton)
            unittest.TestCase.assertRaises(self, expected_exception=TypeError)

        def test_onExecuteButtonClicked_with_input_file(self):
            self.main.openFileLineEdit.setText("test_files/benzene.xyz")
            QTest.mouseClick(self.main.generateInputFileButton, Qt.LeftButton)
            QTest.mouseClick(self.main.executeButton, Qt.LeftButton)
            self.main.writeToLogs.assert_called()
            self.assertEqual(len(self.main.transSelected), 0)
            self.assertEqual(len(self.main.currentSelectedA), 0)
            self.assertEqual(len(self.main.currentSelectedB), 0)

        def test_onTransExecuteButtonClicked(self):
            QTest.mouseClick(self.main.generateTransInputFileButton, Qt.LeftButton)
            QTest.mouseClick(self.main.executeTransButton, Qt.LeftButton)

        def test_onExecuteCurrButtonClicked(self):
            QTest.mouseClick(self.main.generateCurrInputFileButton, Qt.LeftButton)
            QTest.mouseClick(self.main.executeCurrButton, Qt.LeftButton)

        def test_onExecuteCurrGraphButtonClicked(self):
            QTest.mouseClick(self.main.executeCurrGraphButton, Qt.LeftButton)

        def test_onExecute3DGraphButtonClicked(self):
            QTest.mouseClick(self.main.execute3DGraphButton, Qt.LeftButton)

    def test_onGenerateInputFileButtonClicked_and_file_exists(self):
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateInputFileButton, Qt.LeftButton)
        with open("test_files/correct.in") as correct:
            self.assertEqual(correct.read(), self.main.inputTextEdit.toPlainText())
        self.main.writeToLogs.assert_called_with(
            "Input file " + file_in_cur_dir("benzene.in") + ".in generated successfully.", "green")

    def test_onGenerateInputFileButtonClicked_with_nonexistent_xyz(self):
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

    def test_onGenerateTransInputFileButtonClicked_and_file_exists(self):
        self.main.transSelected = {"1": ["1", "2", "3"], "2": ["4", "5"], "3": ["6"], "4": [], "5": ["9"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateTransInputFileButton, Qt.LeftButton)
        with open("test_files/correct_trans.in") as correct:
            self.assertEqual(correct.read(), self.main.inputTextEdit.toPlainText())
        self.main.writeToLogs.assert_called_with(
            "Transmission input file " + file_in_cur_dir(".in") + ".in generated successfully.", "green")

    def test_onGenerateTransInputFileButtonClicked_and_gamma_is_none(self):
        self.main.transSelected = {"1": ["1", "2", "3"], "2": ["4", "5"], "3": ["6"], "4": [], "5": ["9"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        self.main.gammaLineEdit.setText("")
        QTest.mouseClick(self.main.generateTransInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with("Error: Missing input for gamma.")
        unittest.TestCase.assertRaises(self, expected_exception=ValueError)

    def test_onGenerateTransInputFileButtonClicked_with_nonexistent_default_input(self):
        os.remove("config/default_trans.in")
        self.main.transSelected = {"1": ["1", "2", "3"], "2": ["4", "5"], "3": ["6"], "4": [], "5": ["9"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateTransInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with(
            "Error: No default input file found, check that config/default_trans.in exists.")
        unittest.TestCase.assertRaises(self, expected_exception=FileNotFoundError)
        copy_file_from_main_config("config/default_trans.in")

    def test_onGenerateTransInputFileButtonClicked_with_nonexistent_xyz(self):
        self.main.transSelected = {"1": ["1", "2", "3"], "2": ["4", "5"], "3": ["6"], "4": [], "5": ["9"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/nonexistent.xyz")
        QTest.mouseClick(self.main.generateTransInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with(
            "Error: No .xyz file selected to generate Plato input file.")
        unittest.TestCase.assertRaises(self, expected_exception=IOError)

    def test_onGenerateTransInputFileButtonClicked_with_insufficient_terminals(self):
        self.main.transSelected = {"1": ["1", "2", "3"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateTransInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with(
            "Error: Insufficient terminals selected (min. two required). Select terminals by left clicking atoms.")
        unittest.TestCase.assertRaises(self, expected_exception=AssertionError)

    def test_onGenerateCurrInputFileButtonClicked_and_file_exists(self):
        self.main.transSelected = {"1": ["1", "2", "3"], "3": ["6"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateCurrInputFileButton, Qt.LeftButton)
        with open("test_files/correct_curr.in") as correct:
            self.assertEqual(correct.read(), self.main.inputTextEdit.toPlainText())
        self.main.writeToLogs.assert_called_with(
            "Current input file " + file_in_cur_dir(".in") + ".in generated successfully.", "green")

    def test_onGenerateCurrInputFileButtonClicked_and_bias_is_none(self):
        self.main.transSelected = {"1": ["1", "2", "3"], "2": ["4", "5"], "3": ["6"], "4": [], "5": ["9"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        self.main.biasLineEdit.setText("")
        QTest.mouseClick(self.main.generateCurrInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with("Error: Missing input for bias.")
        unittest.TestCase.assertRaises(self, expected_exception=ValueError)

    def test_onGenerateCurrInputFileButtonClicked_and_reference_pot_is_none(self):
        self.main.transSelected = {"1": ["1", "2", "3"], "2": ["4", "5"], "3": ["6"], "4": [], "5": ["9"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        self.main.referenceLineEdit.setText("")
        QTest.mouseClick(self.main.generateCurrInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with("Error: Missing input for reference potential.")
        unittest.TestCase.assertRaises(self, expected_exception=ValueError)

    def test_onGenerateCurrInputFileButtonClicked_with_nonexistent_default_input(self):
        os.remove("config/default_curr.in")
        self.main.transSelected = {"1": ["1", "2", "3"], "3": ["4", "5"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateCurrInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with(
            "Error: No default current input file found, check that config/default_curr.in exists.")
        unittest.TestCase.assertRaises(self, expected_exception=FileNotFoundError)
        copy_file_from_main_config("config/default_curr.in")

    def test_onGenerateCurrInputFileButtonClicked_with_nonexistent_xyz(self):
        self.main.transSelected = {"1": ["1", "2", "3"], "2": ["4", "5"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/nonexistent.xyz")
        QTest.mouseClick(self.main.generateCurrInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with(
            "Error: No .xyz file selected to generate Plato input file.")
        unittest.TestCase.assertRaises(self, expected_exception=IOError)

    def test_onGenerateCurrInputFileButtonClicked_with_insufficient_terminals(self):
        self.main.transSelected = {"1": ["1", "2", "3"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateCurrInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with(
            "Error: Insufficient terminals selected (two required). Select terminals by left clicking atoms.")
        unittest.TestCase.assertRaises(self, expected_exception=AssertionError)

    def test_onGenerateCurrInputFileButtonClicked_with_incorrect_terminals(self):
        self.main.transSelected = {"1": ["1", "2", "3"], "2": ["4", "5"], "3": ["6"], "4": [], "5": ["9"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateCurrInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with(
            "Error: Incorrect number of terminals selected, may only calculate current between two terminals.")
        unittest.TestCase.assertRaises(self, expected_exception=NotImplementedError)

    def test_onGenerateCurrInputFileButtonClicked_with_insufficient_region_A(self):
        self.main.transSelected = {"1": ["1", "2", "3"], "2": ["4", "5"]}
        self.main.currentSelectedA = []
        self.main.currentSelectedB = ["7", "8", "9"]
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateCurrInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with(
            "Error: Insufficient atoms for region A (min. one required). Select atoms for A by middle clicking.")
        unittest.TestCase.assertRaises(self, expected_exception=ValueError)

    def test_onGenerateCurrInputFileButtonClicked_with_insufficient_region_B(self):
        self.main.transSelected = {"1": ["1", "2", "3"], "2": ["4", "5"]}
        self.main.currentSelectedA = ["4", "5", "6"]
        self.main.currentSelectedB = []
        self.main.openFileLineEdit.setText("test_files/benzene.xyz")
        QTest.mouseClick(self.main.generateCurrInputFileButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with(
            "Error: Insufficient atoms for region B (min. one required). Select atoms for B by middle clicking.")
        unittest.TestCase.assertRaises(self, expected_exception=ZeroDivisionError)

    def test_onOpenFileButtonClicked(self):
        pass
        # QTest.mouseClick(self.main.openFileButton, Qt.LeftButton)
        # self.assertEqual(self.main.openFileLineEdit.text(), "C:/Users/Aaron Lam/Downloads/Platomic/tests/test_files/benzene.xyz")

    def test_onOpenOutFileButtonClicked(self):
        pass
        # QTest.mouseClick(self.main.openOutFileButton, Qt.LeftButton)
        # self.assertEqual(self.main.openOutFileLineEdit.text(), "C:/Users/Aaron Lam/Downloads/Platomic/tests/config/benzene.out")

    def test_onOpenWfFileButtonClicked(self):
        pass
        # QTest.mouseClick(self.main.openWfFileButton, Qt.LeftButton)
        # self.assertEqual(self.main.openWfFileLineEdit.text(), "C:/Users/Aaron Lam/Downloads/Platomic/tests/config/benzene.wf")

    def test_onOpenCsvFileButtonClicked(self):
        pass
        # QTest.mouseClick(self.main.openCsvFileButton, Qt.LeftButton)
        # self.assertEqual(self.main.openCsvFileLineEdit.text(), "C:/Users/Aaron Lam/Downloads/Platomic/tests/test_files/test_csv.csv")

    def test_onOpenDirButtonClicked(self):
        pass
        # QTest.mouseClick(self.main.openDirButton, Qt.LeftButton)
        # self.assertEqual(self.main.openDirLineEdit.text(), "C:/Users/Aaron Lam/Downloads/Platomic/tests/test_files/test_out_dir")

    def test_onOpenDirGammaButtonClicked(self):
        pass
        # QTest.mouseClick(self.main.openDirGammaButton, Qt.LeftButton)
        # self.assertEqual(self.main.gammaOpenDirLineEdit.text(), "C:/Users/Aaron Lam/Downloads/Platomic/tests/test_files/test_trans_dir")

    def test_onExecuteLoadedButtonClicked(self):
        self.main.openOutFileLineEdit.setText("config/benzene.out")
        self.main.openWfFileLineEdit.setText("config/benzene.wf")
        QTest.mouseClick(self.main.executeLoadedButton, Qt.LeftButton)
        self.main.draw.assert_called_once()
        self.main.writeToLogs.assert_called_with("Execution carried out successfully.", "green")
        self.assertEqual(return_occupied_keys(self.main.transSelected), 0)
        self.assertEqual(len(self.main.currentSelectedA), 0)
        self.assertEqual(len(self.main.currentSelectedB), 0)

    def test_onExecuteLoadedButtonClicked_with_no_out_file(self):
        self.main.openWfFileLineEdit.setText("config/benzene.wf")
        QTest.mouseClick(self.main.executeLoadedButton, Qt.LeftButton)
        self.main.draw.assert_not_called()
        self.main.writeToLogs.assert_not_called()
        self.main.writeErrorToLogs.assert_called_with("Error: no Plato output file (.out) selected.")

    def test_onExecuteLoadedButtonClicked_with_no_wf_file(self):
        self.main.openOutFileLineEdit.setText("config/benzene.out")
        QTest.mouseClick(self.main.executeLoadedButton, Qt.LeftButton)
        self.main.draw.assert_not_called()
        self.main.writeToLogs.assert_not_called()
        self.main.writeErrorToLogs.assert_called_with("Error: no Plato wavefunction file (.wf) selected.")

    def test_onTransExecuteLoadedButtonClicked(self):
        self.main.openCsvFileLineEdit.setText("test_files/test_csv.csv")
        QTest.mouseClick(self.main.transExecuteLoadedButton, Qt.LeftButton)
        self.main.writeToLogs.assert_called_with("Graphs plotted successfully.", "green")
        self.assertEqual(self.main.csvFilename, self.main.openCsvFileLineEdit.text())
        self.main.graphComboBox.clear.assert_called_once()
        self.main.graphComboBox.addItems.assert_called_once()

    def test_onTransExecuteLoadedButtonClicked_with_no_csv(self):
        QTest.mouseClick(self.main.transExecuteLoadedButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with("Error: no Plato generated csv file (.csv) selected.")
        self.main.writeToLogs.assert_not_called()
        self.main.graphComboBox.clear.assert_not_called()
        self.main.graphComboBox.addItems.assert_not_called()

    def test_onCurrExecuteLoadedButtonClicked(self):
        self.main.openDirLineEdit.setText("test_files/test_out_dir")
        QTest.mouseClick(self.main.currExecuteLoadedButton, Qt.LeftButton)
        self.main.writeToLogs.assert_called_with("Current vs. bias graph plotted successfully.", "green")

    def test_onCurrExecuteLoadedButtonClicked_with_no_dir(self):
        QTest.mouseClick(self.main.currExecuteLoadedButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with("Error: no directory selected.")
        self.main.writeToLogs.assert_not_called()

    def test_onGammaExecuteLoadedButtonClicked(self):
        self.main.gammaOpenDirLineEdit.setText("test_files/test_trans_dir")
        QTest.mouseClick(self.main.gammaExecuteLoadedButton, Qt.LeftButton)
        self.main.writeToLogs.assert_called_with("Energy vs. gamma vs. transmission graph plotted successfully.", "green")

    def test_onGammaExecuteLoadedButtonClicked_with_no_dir(self):
        QTest.mouseClick(self.main.gammaExecuteLoadedButton, Qt.LeftButton)
        self.main.writeErrorToLogs.assert_called_with("Error: no directory selected.")
        self.main.writeToLogs.assert_not_called()

    def test_onSwitchToInputFileTabButtonClicked(self):
        QTest.mouseClick(self.main.switchToInputFileTabButton, Qt.LeftButton)
        self.assertEqual(self.main.mainWindow.currentIndex(), 4)

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
        self.main.bondColSlider.setValue(30)
        self.assertIs(self.main.bondCol, 30)
        self.assertEqual(self.main.bondColSliderLabel.text(), "Columns: 30")
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

    def test_setCheckBoxIndex(self):
        self.main.checkBoxIndex.setChecked(False)
        self.main.openGLWidget.update.assert_called_once()
        self.assertEqual(self.main.openGLWidget.index, False)

    def test_setCheckBoxSymbol(self):
        self.main.checkBoxSymbol.setChecked(True)
        self.main.openGLWidget.update.assert_called_once()
        self.assertTrue(self.main.openGLWidget.symbol)

    def test_setCheckBoxPosition(self):
        self.main.checkBoxPosition.setChecked(True)
        self.main.openGLWidget.update.assert_called_once()
        self.assertTrue(self.main.openGLWidget.position)

    def test_setCheckBoxRadius(self):
        self.main.checkBoxRadius.setChecked(True)
        self.main.openGLWidget.update.assert_called_once()
        self.assertTrue(self.main.openGLWidget.radius)

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
        self.assertEqual(self.main.mainWindow.currentIndex(), 5)

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

    def test_setHorizontalSliderOrbitalLabel(self):
        self.main.horizontalSlider.setValue(5)
        self.assertIs(self.main.mode, 5)
        self.assertEqual(self.main.horizontalSliderLabel.text(), "Molecular Orbital: 6")
        self.main.draw.assert_called_once()

    def test_setHorizontalSliderEnergyLabel(self):
        self.main.horizontalSlider.setValue(6)
        self.assertIs(self.main.mode, 6)
        self.assertEqual(self.main.horizontalSliderEnergyLabel.text(), "Energy (eV): -11.7604")
        self.main.draw.assert_called_once()

    def test_onTransSelection(self):
        QTest.mouseClick(self.main.openGLWidget, Qt.LeftButton, pos=QPoint(300, 300))
        self.assertEqual(self.main.transSelected, {"1": ["11"], "2": [], "3": [], "4": [], "5": []})
        self.assertEqual(self.main.atoms[10].get_isSelectedTrans(), 1)
        self.main.draw.assert_called_once()
        self.main.writeToLogs.assert_called()

    def test_onCurrentSelectionA_none(self):
        QTest.mouseClick(self.main.openGLWidget, Qt.RightButton, pos=QPoint(300, 300))
        QTest.mouseClick(self.main.openGLWidget, Qt.RightButton, pos=QPoint(300, 300))
        self.assertEqual(len(self.main.currentSelectedA), 0)
        self.main.writeToLogs.assert_called_with("No regions selected.", "purple")

    def test_onCurrentSelectionB_none(self):
        QTest.mouseClick(self.main.openGLWidget, Qt.MiddleButton, pos=QPoint(300, 300))
        QTest.mouseClick(self.main.openGLWidget, Qt.MiddleButton, pos=QPoint(300, 300))
        self.assertEqual(len(self.main.currentSelectedB), 0)
        self.main.writeToLogs.assert_called_with("No regions selected.", "lime")

    def test_onCurrentSelectionA(self):
        QTest.mouseClick(self.main.openGLWidget, Qt.RightButton, pos=QPoint(300, 300))
        self.assertTrue(self.main.atoms[10].get_isSelectedCurrA())
        self.main.draw.assert_called_once()
        self.main.writeToLogs.assert_called()

    def test_onCurrentSelectionB(self):
        QTest.mouseClick(self.main.openGLWidget, Qt.MiddleButton, pos=QPoint(300, 300))
        self.assertTrue(self.main.atoms[10].get_isSelectedCurrB())
        self.main.draw.assert_called_once()
        self.main.writeToLogs.assert_called()

    def test_onResetViewButtonClicked(self):
        QTest.mouseClick(self.main.resetViewButton, Qt.LeftButton)
        self.main.openGLWidget.reset.assert_called_once()
        self.main.openGLWidget.setBackgroundColor.assert_called_once()
        self.main.writeToLogs.assert_called_once()

    def test_onSaveImageButtonClicked(self):
        pass
        # QTest.mouseClick(self.main.saveImageButton, Qt.LeftButton)
        # self.assertTrue(filecmp.cmp("correct.png", "test_files/correct.png"))
        # os.remove("correct.png")

    def test_onToggleAtomsButtonClicked_on(self):
        QTest.mouseClick(self.main.toggleAtomsButton, Qt.LeftButton)
        self.main.writeToLogs.assert_called_with("Atoms toggled off.", "grey")
        self.main.draw.assert_called_once()

    def test_onToggleAtomsButtonClicked_off(self):
        self.main.toggleAtomsButton.setChecked(True)
        QTest.mouseClick(self.main.toggleAtomsButton, Qt.LeftButton)
        self.main.writeToLogs.assert_called_with("Atoms toggled on.", "grey")
        self.main.draw.assert_called_once()

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

    def test_onGammaLineEditChanged(self):
        self.main.gammaLineEdit.setText("1")
        self.main.onGammaLineEditChanged()
        self.assertEqual(self.main.gammaLineEdit.text(), "1")
        self.assertEqual(self.main.gammaLineEdit2.text(), "1")

    def test_onGammaLineEditChanged_invalid(self):
        self.main.gammaLineEdit.setText("-1")
        self.main.onGammaLineEditChanged()
        self.main.writeErrorToLogs.assert_called_with("Error: non-positive float '-1' entered for gamma.")
        self.assertEqual(self.main.gammaLineEdit.text(), "")
        self.assertEqual(self.main.gammaLineEdit2.text(), "")

    def test_onGammaLineEditChanged2(self):
        self.main.gammaLineEdit2.setText("2")
        self.main.onGammaLineEditChanged2()
        self.assertEqual(self.main.gammaLineEdit.text(), "2")
        self.assertEqual(self.main.gammaLineEdit2.text(), "2")

    def test_onGammaLineEditChanged2_invalid(self):
        self.main.gammaLineEdit2.setText("-2")
        self.main.onGammaLineEditChanged2()
        self.main.writeErrorToLogs.assert_called_with("Error: non-positive float '-2' entered for gamma.")
        self.assertEqual(self.main.gammaLineEdit.text(), "")
        self.assertEqual(self.main.gammaLineEdit2.text(), "")

    def test_onReferenceLineEditChanged(self):
        self.main.referenceLineEdit.setText("-0.812")
        self.main.onReferenceLineEditChanged()
        self.assertEqual(self.main.referenceLineEdit.text(), "-0.812")

    def test_onReferenceLineEditChanged_invalid(self):
        self.main.referenceLineEdit.setText("abc")
        self.main.onReferenceLineEditChanged()
        self.main.writeErrorToLogs.assert_called_with("Error: non-float 'abc' entered for reference potential.")
        self.assertEqual(self.main.referenceLineEdit.text(), "")

    def test_onBiasLineEditChanged(self):
        self.main.biasLineEdit.setText("-0.423")
        self.main.onBiasLineEditChanged()
        self.assertEqual(self.main.biasLineEdit.text(), "-0.423")

    def test_onBiasLineEditChanged_invalid(self):
        self.main.biasLineEdit.setText("abc")
        self.main.onBiasLineEditChanged()
        self.main.writeErrorToLogs.assert_called_with("Error: non-float 'abc' entered for bias.")
        self.assertEqual(self.main.biasLineEdit.text(), "")

    def test_onStepsLineEditChanged(self):
        self.main.stepsLineEdit.setText("20")
        self.main.onStepsLineEditChanged()
        self.assertEqual(self.main.stepsLineEdit.text(), "20")

    def test_onStepsLineEditChanged_invalid(self):
        self.main.stepsLineEdit.setText("0.5")
        self.main.onStepsLineEditChanged()
        self.main.writeErrorToLogs.assert_called_with("Error: non-natural number '0.5' entered for steps.")
        self.assertEqual(self.main.stepsLineEdit.text(), "")

    def test_onGammaStartLineEditChanged(self):
        self.main.gammaStartLineEdit.setText("1")
        self.main.onGammaStartLineEditChanged()
        self.assertEqual(self.main.gammaStartLineEdit.text(), "1")

    def test_onGammaStartLineEditChanged_invalid(self):
        self.main.gammaStartLineEdit.setText("-1")
        self.main.onGammaStartLineEditChanged()
        self.main.writeErrorToLogs.assert_called_with("Error: non-pos float '-1' entered for gamma start value.")
        self.assertEqual(self.main.gammaStartLineEdit.text(), "")

    def test_onGammaEndLineEditChanged(self):
        self.main.gammaEndLineEdit.setText("3")
        self.main.onGammaEndLineEditChanged()
        self.assertEqual(self.main.gammaEndLineEdit.text(), "3")

    def test_onGammaEndLineEditChanged_invalid(self):
        self.main.gammaEndLineEdit.setText("-3.5")
        self.main.onGammaEndLineEditChanged()
        self.main.writeErrorToLogs.assert_called_with("Error: non-pos float '-3.5' entered for gamma end value.")
        self.assertEqual(self.main.gammaEndLineEdit.text(), "")

    def test_onGammaStepsLineEditChanged(self):
        self.main.gammaStepsLineEdit.setText("10")
        self.main.onGammaStepsLineEditChanged()
        self.assertEqual(self.main.gammaStepsLineEdit.text(), "10")

    def test_onGammaStepsLineEditChanged_invalid(self):
        self.main.gammaStepsLineEdit.setText("0")
        self.main.onGammaStepsLineEditChanged()
        self.main.writeErrorToLogs.assert_called_with("Error: non-natural number '0' entered for gamma steps value.")
        self.assertEqual(self.main.gammaStepsLineEdit.text(), "")

def copy_file_from_main_config(filename):
    with open("../" + filename, 'r') as source:
        with open(filename, 'w') as f:
            for line in source:
                f.write(line)


def file_in_cur_dir(ends_with):
    for file in os.listdir("."):
        if file.endswith(ends_with):
            return os.path.splitext(file)[0]


def cleanUp():
    os.remove("attributes.txt")
    copy_file_from_main_config("config/attributes.txt")
    for file in os.listdir("."):
        if file.endswith(".in"):
            os.remove(os.path.join(".", file))

