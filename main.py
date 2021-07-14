import secrets
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from glview import *
from glview3D import *
from plot import *
from input import *
from subprocess import PIPE, run
import math
import os
import numpy as np
import sys
import pyautogui
import traceback

np.seterr(divide='ignore', invalid='ignore')
resolution = pyautogui.size()
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
app = QtWidgets.QApplication(sys.argv)

default_input = input_file_setup("config/benzene.out", "config/attributes.txt", "config/benzene.wf")


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, screen_width, atoms=None):
        super(MainWindow, self).__init__()

        # Load the UI Page
        uic.loadUi("config/mainwindow5.ui", self)
        self.setWindowTitle("Platomic")
        self.setWindowIcon(QIcon("config/platomic.png"))
        self.multiplier = int(screen_width / 1920)

        # Initialise state
        self.atoms = atoms
        self.csvFilename = None
        self.inputFilename = None
        self.transInputFilename = None
        self.currInputFilename = None
        self.transSelected = {"1": [], "2": [], "3": [], "4": [], "5": []}
        self.currentSelectedA = []
        self.currentSelectedB = []
        self.mode = 0
        self.id = secrets.token_hex(3)

        # Initialise propertiesWindow
        # setupSettingsTab
        # executeButton
        self.executeButton.clicked.connect(self.onExecuteButtonClicked)

        # executeTransButton
        self.executeTransButton.clicked.connect(self.onTransExecuteButtonClicked)

        # executeCurrButton and executeCurrGraphButton
        self.executeCurrButton.clicked.connect(self.onExecuteCurrButtonClicked)
        self.executeCurrGraphButton.clicked.connect(self.onExecuteCurrGraphButtonClicked)
        self.execute3DGraphButton.clicked.connect(self.onExecute3DGraphButtonClicked)

        # executeLoadedButton and transExecuteLoadedButton
        self.executeLoadedButton.clicked.connect(self.onExecuteLoadedButtonClicked)
        self.transExecuteLoadedButton.clicked.connect(self.onTransExecuteLoadedButtonClicked)
        self.currExecuteLoadedButton.clicked.connect(self.onCurrExecuteLoadedButtonClicked)
        self.gammaExecuteLoadedButton.clicked.connect(self.onGammaExecuteLoadedButtonClicked)

        # generateInputFileButton
        self.generateInputFileButton.clicked.connect(self.onGenerateInputFileButtonClicked)

        # generateTransInputFileButton
        self.generateTransInputFileButton.clicked.connect(self.onGenerateTransInputFileButtonClicked)

        # generateCurrInputFileButton
        self.generateCurrInputFileButton.clicked.connect(self.onGenerateCurrInputFileButtonClicked)

        # openFileLineEdit
        # openFileButton
        self.openFileButton.clicked.connect(self.onOpenFileButtonClicked)
        self.openOutFileButton.clicked.connect(self.onOpenOutFileButtonClicked)
        self.openWfFileButton.clicked.connect(self.onOpenWfFileButtonClicked)
        self.openCsvFileButton.clicked.connect(self.onOpenCsvFileButtonClicked)
        self.openDirButton.clicked.connect(self.onOpenDirButtonClicked)
        self.openDirGammaButton.clicked.connect(self.onOpenDirGammaButtonClicked)
        self.gammaLineEdit.editingFinished.connect(self.onGammaLineEditChanged)
        self.gammaLineEdit2.editingFinished.connect(self.onGammaLineEditChanged2)
        self.gammaStartLineEdit.editingFinished.connect(self.onGammaStartLineEditChanged)
        self.gammaEndLineEdit.editingFinished.connect(self.onGammaEndLineEditChanged)
        self.gammaStepsLineEdit.editingFinished.connect(self.onGammaStepsLineEditChanged)
        self.excessLineEdit.editingFinished.connect(self.onExcessLineEditChanged)
        self.referenceLineEdit.editingFinished.connect(self.onReferenceLineEditChanged)
        self.biasLineEdit.editingFinished.connect(self.onBiasLineEditChanged)
        self.stepsLineEdit.editingFinished.connect(self.onStepsLineEditChanged)

        # switchToInputFileTabButton
        self.switchToInputFileTabButton.clicked.connect(self.onSwitchToInputFileTabButtonClicked)

        # checkBoxIndex
        # checkBoxSymbol
        # checkBoxPosition
        # checkBoxRadius
        # fontComboBox
        # sizeComboBox
        # offsetComboBox
        # colourComboBox
        self.checkBoxIndex.stateChanged.connect(self.setCheckBoxIndex)
        self.checkBoxSymbol.stateChanged.connect(self.setCheckBoxSymbol)
        self.checkBoxPosition.stateChanged.connect(self.setCheckBoxPosition)
        self.checkBoxRadius.stateChanged.connect(self.setCheckBoxRadius)

        self.fontComboBox.currentIndexChanged.connect(self.setFontComboBox)
        self.sizeComboBox.currentIndexChanged.connect(self.setSizeComboBox)
        self.offsetComboBox.currentIndexChanged.connect(self.setOffsetComboBox)
        self.colourComboBox.currentIndexChanged.connect(self.setColourComboBox)

        self.fontComboBox.addItems(["Arial", "Cambria", "Helvetica", "Times New Roman"])
        self.sizeComboBox.addItems(["14", "16", "18", "20", "24", "30", "42"])
        self.offsetComboBox.addItems(["X", "Y", "Z"])
        self.colourComboBox.addItems(["Orange", "Red", "Lime", "Blue", "Purple", "Yellow"])
        self.openGLWidget.font = "Arial"
        self.openGLWidget.size = 14
        self.openGLWidget.offset = 0
        self.openGLWidget.colour = "Orange"

        # graphSettingsTab and terminalComboBox
        self.graphComboBox.currentIndexChanged.connect(self.setGraphComboBox)
        self.terminalComboBox.currentIndexChanged.connect(self.setTerminalComboBox)
        self.terminalComboBox.addItems(["Terminal 1", "Terminal 2", "Terminal 3", "Terminal 4", "Terminal 5"])
        self.graphKeys = None

        # atomSettingsTab
        # atomColSlider
        self.atomCol = self.atomColSlider.value()
        # atomColSliderLabel
        self.atomColSlider.sliderReleased.connect(self.setAtomColSliderLabel)
        self.atomColSlider.valueChanged.connect(self.updateAtomColSliderLabel)

        # atomRowSlider
        self.atomRow = self.atomRowSlider.value()
        # atomRowSliderLabel
        self.atomRowSlider.sliderReleased.connect(self.setAtomRowSliderLabel)
        self.atomRowSlider.valueChanged.connect(self.updateAtomRowSliderLabel)

        # bondColSlider
        self.bondCol = self.bondColSlider.value()
        # bondColSliderLabel
        self.bondColSlider.sliderReleased.connect(self.setBondColSliderLabel)
        self.bondColSlider.valueChanged.connect(self.updateBondColSliderLabel)

        # bondRowSlider
        self.bondRow = self.bondRowSlider.value()
        # bondRowSliderLabel
        self.bondRowSlider.sliderReleased.connect(self.setBondRowSliderLabel)
        self.bondRowSlider.valueChanged.connect(self.updateBondRowSliderLabel)

        # brightnessSlider
        # brightnessSliderLabel
        self.brightnessSlider.sliderReleased.connect(self.setBrightnessSliderLabel)
        self.brightnessSlider.valueChanged.connect(self.updateBrightnessSliderLabel)

        # bondRadiusSlider
        self.bondRadius = 0.15
        # bondRadiusSliderLabel
        self.bondRadiusSlider.sliderReleased.connect(self.setBondRadiusSliderLabel)
        self.bondRadiusSlider.valueChanged.connect(self.updateBondRadiusSliderLabel)

        # bondThresholdSlider
        self.bondThreshold = 5.0
        # bondThersholdSliderlabel
        self.bondThresholdSlider.sliderReleased.connect(self.setBondThresholdSliderLabel)
        self.bondThresholdSlider.valueChanged.connect(self.updateBondThresholdSliderLabel)

        # switchToAttrFileTabButton
        self.switchToAttrFileTabButton.clicked.connect(self.onSwitchToAttrFileTabButtonClicked)

        # orbitalSettingsTab
        # advOrbWfCheckBox
        self.advOrbWfCheckBox.stateChanged.connect(self.draw)

        # advOrbHorzCheckBox
        self.advOrbHorzCheckBox.stateChanged.connect(self.draw)

        # advOrbVertCheckBox
        self.advOrbVertCheckBox.stateChanged.connect(self.draw)

        # sphOrbWfCheckBox
        self.sphOrbWfCheckBox.stateChanged.connect(self.draw)

        # sphOrbFacesCheckBox
        self.sphOrbFacesCheckBox.stateChanged.connect(self.draw)

        # advOrbFacesCheckBox
        self.advOrbFacesCheckBox.stateChanged.connect(self.draw)

        # orbColSlider
        self.orbCol = self.orbColSlider.value()
        # orbColSliderLabel
        self.orbColSlider.sliderReleased.connect(self.setOrbColSliderLabel)
        self.orbColSlider.valueChanged.connect(self.updateOrbColSliderLabel)

        # orbRowSlider
        self.orbRow = self.orbRowSlider.value()
        # orbRowSliderLabel
        self.orbRowSlider.sliderReleased.connect(self.setOrbRowSliderLabel)
        self.orbRowSlider.valueChanged.connect(self.updateOrbRowSliderLabel)

        # orbScalerSlider
        self.orbScaler = self.orbScalerSlider.value()
        # orbScalerSliderLabel
        self.orbScalerSlider.sliderReleased.connect(self.setScalerSliderLabel)
        self.orbScalerSlider.valueChanged.connect(self.updateScalerSliderLabel)

        # thetaSlider
        self.theta = self.thetaSlider.value()
        # thetaSliderLabel
        self.thetaSlider.sliderReleased.connect(self.setThetaSliderLabel)
        self.thetaSlider.valueChanged.connect(self.updateThetaSliderLabel)

        # phiSlider
        self.phi = math.radians(self.phiSlider.value())
        # phiSliderLabel
        self.phiSlider.sliderReleased.connect(self.setPhiSliderLabel)
        self.phiSlider.valueChanged.connect(self.updatePhiSliderLabel)

        # colourXSlider
        self.R = 1.00
        self.G = 0.00
        self.B = 1.00
        self.A = 0.50
        self.colourRSlider.sliderReleased.connect(self.setColourRSliderLabel)
        self.colourGSlider.sliderReleased.connect(self.setColourGSliderLabel)
        self.colourBSlider.sliderReleased.connect(self.setColourBSliderLabel)
        self.colourASlider.sliderReleased.connect(self.setColourASliderLabel)
        self.colourRSlider.valueChanged.connect(self.updateColourRSliderLabel)
        self.colourGSlider.valueChanged.connect(self.updateColourGSliderLabel)
        self.colourBSlider.valueChanged.connect(self.updateColourBSliderLabel)
        self.colourASlider.valueChanged.connect(self.updateColourASliderLabel)

        # Initialise mainWindow

        # mainDisplayTab
        # horizontalSlider
        # horizontalSliderLabel
        self.horizontalSlider.sliderReleased.connect(self.setHorizontalSliderLabel)
        self.horizontalSlider.valueChanged.connect(self.updateHorizontalSliderLabel)

        # openGLWidget and gammaGLWidget
        self.openGLWidget.opts['distance'] = 15
        self.gammaGLWidget.opts['distance'] = 5
        self.openGLWidget.multiplier = self.multiplier
        self.gammaGLWidget.multiplier = self.multiplier
        if self.atoms is None:
            self.openGLWidget.atoms = [
                Atom("0", 0, -9, 0,
                     "Welcome to Platomic. To get started, select an .xyz file in the 'Plato setup' tab."),
                Atom("0", 0, -9.25, -1, "Hover over any (?) icons for help and / or additional information."),
                Atom("0", 0, -9.5, -2, "For a full in-depth tutorial check out the User Guide.")]
        else:
            self.openGLWidget.atoms = self.atoms
            self.draw()
        self.backgroundColor = (40, 40, 40)
        self.openGLWidget.setBackgroundColor(self.backgroundColor)
        self.openGLWidget.left_clicked.connect(self.onTransSelection)
        self.openGLWidget.right_clicked.connect(self.onCurrentSelectionA)
        self.openGLWidget.middle_clicked.connect(self.onCurrentSelectionB)

        # resetViewButton
        self.resetViewButton.clicked.connect(self.onResetViewButtonClicked)

        # saveImageButton, save3DImageButton
        self.saveImageButton.clicked.connect(self.onSaveImageButtonClicked)
        self.save3DImageButton.clicked.connect(self.onSave3DImageButtonClicked)

        # toggleAtomsButton
        self.toggleAtomsButton.clicked.connect(self.onToggleAtomsButtonClicked)

        # inputFileTab
        # inputTextEdit
        # saveInputFileButton
        self.saveInputFileButton.clicked.connect(self.onSaveInputFileButtonClicked)

        # AttributeFileTab
        # attributeTextEdit
        with open("config/attributes.txt", "r") as f:
            contents = f.readlines()
        for line, content in enumerate(contents):
            self.attributeTextEdit.insertPlainText(content)

        # saveAttributeFileButton
        self.saveAttributeFileButton.clicked.connect(self.onSaveAttributeFileButtonClicked)

        # fullConsoleTab
        # fullConsoleTextEdit

    # Initialise functions
    # Initialise propertiesWindow
    # setupSettingsTab
    # executeButton

    def execute(self, verbose=True):
        if os.name == 'nt':
            self.writeErrorToLogs("Plato back-end execution is not supported on Windows systems.")
            return False
        try:
            command = "(cd ./Plato/bin && ./tb1 ../../" + self.inputFilename + ")"
        except TypeError:
            self.writeErrorToLogs("No Plato input file found, click generate before clicking execute.")
            return False
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if result.returncode and verbose:
            self.writeToLogs(result.stderr, "red")
            if result.stdout and verbose:
                self.writeToLogs(result.stdout, "red")
            return False
        if result.stdout and verbose:
            self.writeToLogs(result.stdout, "black")
        return True

    def onExecuteButtonClicked(self):
        self.writeToLogs("Starting execution.", "green")
        if not self.execute():
            return
        self.atoms = input_file_setup(self.inputFilename + ".out", "config/attributes.txt", self.inputFilename + ".wf")
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(self.atoms[0].get_total_orbitals() - 1)
        self.openGLWidget.atoms = self.atoms
        self.draw()
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.mainDisplayTab))
        self.propertiesWindow.setCurrentIndex(self.propertiesWindow.indexOf(self.displaySettingsTab))
        self.writeToLogs("Execution carried out successfully.\n", "green")
        self.transSelected = {"1": [], "2": [], "3": [], "4": [], "5": []}
        self.currentSelectedA = []
        self.currentSelectedB = []
        self.executeButton.setEnabled(False)
        self.id = secrets.token_hex(3)

    def onTransExecuteButtonClicked(self):
        self.writeToLogs("Starting transmission execution.", "green")
        if not self.execute():
            return
        self.writeToLogs("Execution carried out successfully.", "green")
        self.csvFilename = self.inputFilename + "_trans.csv"
        headers_mapped, headers = transmission_headers(self.csvFilename, self.transSelected)
        self.graphKeys = headers
        self.graphComboBox.clear()
        self.graphComboBox.addItems(headers_mapped)
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.graphTab))
        self.propertiesWindow.setCurrentIndex(self.propertiesWindow.indexOf(self.graphSettingsTab))
        self.writeToLogs("Graphs plotted successfully.\n", "green")
        self.executeTransButton.setEnabled(False)
        self.id = secrets.token_hex(3)

    def onExecuteCurrButtonClicked(self, boolean, verbose=True):
        self.writeToLogs("Starting current execution.", "green")
        if not self.execute(verbose):
            return
        current = find_current_in_file(self.inputFilename + ".out")
        if verbose:
            self.writeToLogs("Execution carried out successfully.", "green")
            self.writeToLogs("Current: " + current + " mA.\n", "green")
        self.executeCurrButton.setEnabled(False)
        self.id = secrets.token_hex(3)
        return float(current)

    def onExecuteCurrGraphButtonClicked(self):
        self.writeToLogs("Starting current graph execution.", "green")
        try:
            steps = int(self.stepsLineEdit.text())
        except ValueError:
            self.writeErrorToLogs("Error: Missing input for steps.")
            return
        try:
            bias = float(self.biasLineEdit.text())
        except ValueError:
            self.writeErrorToLogs("Error: Missing input for maximum bias.")
            return

        occupied_keys = return_occupied_keys(self.transSelected)
        if not occupied_keys == 2:
            self.writeErrorToLogs(
                "Error: Incorrect number of terminals selected, may only calculate current between two terminals.")
            return
        if len(self.currentSelectedA) <= 0:
            self.writeErrorToLogs(
                "Error: Insufficient atoms for region A (min. one required). Select atoms for A by right clicking.")
            return
        if len(self.currentSelectedB) <= 0:
            self.writeErrorToLogs(
                "Error: Insufficient atoms for region B (min. one required). Select atoms for B by middle clicking.")
            return
        currents = []
        biases = np.linspace(0, bias, steps)
        self.writeToLogs("Starting " + str(steps) + " current calculations.", "green")
        self.id = secrets.token_hex(3)
        ind = 1
        for i in biases:
            bias_i = round(i, 4)
            if not self.onGenerateCurrInputFileButtonClicked(False, False, bias=bias_i):
                return
            currents.append(self.onExecuteCurrButtonClicked(False, False))
            self.writeToLogs(str(ind) + "/" + str(steps) + " transmission calculation completed.", "green")
            QApplication.processEvents()
            ind += 1
        self.writeToLogs("All current calculations completed successfully.", "green")
        current_graph(self.graphWidget2, biases, currents)
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.graphTab2))
        # self.propertiesWindow.setCurrentIndex(self.propertiesWindow.indexOf(self.graphSettingsTab))
        self.writeToLogs("Current vs. bias graph plotted successfully.\n", "green")

    def onExecute3DGraphButtonClicked(self):
        self.writeToLogs("Starting 3D transmission graph execution.", "green")
        self.gammaGLWidget.clear()
        occupied_keys = return_occupied_keys(self.transSelected)
        if not occupied_keys == 2:
            self.writeErrorToLogs(
                "Error: Incorrect number of terminals selected, may only plot 3D graph between two terminals.")
            return
        try:
            gamma_start = float(self.gammaStartLineEdit.text())
        except ValueError:
            self.writeErrorToLogs("Error: Missing input for gamma minimum.")
            return
        try:
            gamma_end = float(self.gammaEndLineEdit.text())
        except ValueError:
            self.writeErrorToLogs("Error: Missing input for gamma maximum.")
            return
        try:
            gamma_steps = int(self.gammaStepsLineEdit.text())
        except ValueError:
            self.writeErrorToLogs("Error: Missing input for gamma steps.")
            return
        interval = (gamma_end - gamma_start) / gamma_steps
        if interval <= 0:
            self.writeErrorToLogs(
                "Error: Difference between Gamma minimum and maximum must be positive and greater than 0.")
            return
        self.writeToLogs("Starting " + str(gamma_steps) + " transmission calculations.", "green")
        self.id = secrets.token_hex(3)
        i = 1
        for gamma in np.linspace(gamma_start, gamma_end, gamma_steps):
            if not self.onGenerateTransInputFileButtonClicked(verbose=False, gamma=round(gamma, 5), step_size=interval):
                return
            self.execute(verbose=False)
            self.writeToLogs(str(i) + "/" + str(gamma_steps) + " transmission calculation completed.", "green")
            QApplication.processEvents()
            i += 1
        self.writeToLogs("All transmission calculations completed successfully.", "green")
        energy, gamma, transmission = process_energy_gamma_trans_csv(".", self.id)
        energy_gamma_trans_graph(self.gammaGLWidget, energy, gamma, transmission)
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.gammaGraphTab))
        self.propertiesWindow.setCurrentIndex(self.propertiesWindow.indexOf(self.graphSettingsTab))
        self.writeToLogs("Energy vs. gamma vs. transmission graph plotted successfully.\n", "green")

    # generateInputFileButton

    def replaceTextEdit(self, filename):
        self.inputTextEdit.clear()
        with open(filename + ".in", "r") as f:
            contents = f.readlines()
        for line, content in enumerate(contents):
            self.inputTextEdit.insertPlainText(content)

    def onGenerateInputFileButtonClicked(self):
        try:
            excess = float(self.excessLineEdit.text())
        except ValueError:
            self.writeErrorToLogs("Error: Missing input for excess electrons.")
            return
        try:
            filename = xyz_to_plato_input(self.openFileLineEdit.text(), excess, self.id)
            self.inputFilename = filename
            self.replaceTextEdit(filename)
        except FileNotFoundError:
            self.writeErrorToLogs("Error: No default input file found, check that config/default.in exists.")
            return
        except IOError:
            self.writeErrorToLogs("Error: No .xyz file selected to generate Plato input file.")
            return
        self.writeToLogs("Input file " + self.inputFilename + ".in generated successfully.\n", "green")
        self.executeButton.setEnabled(True)

    def onGenerateTransInputFileButtonClicked(self, boolean=False, verbose=True, gamma=None, step_size=0.003):
        if gamma is None:
            try:
                gamma = float(self.gammaLineEdit.text())
            except ValueError:
                self.writeErrorToLogs("Error: Missing input for gamma.")
                return False
        try:
            excess = float(self.excessLineEdit.text())
        except ValueError:
            self.writeErrorToLogs("Error: Missing input for excess electrons.")
            return
        try:
            filename = trans_plato_input(self.openFileLineEdit.text(), self.transSelected, excess, gamma, step_size, self.id)
            self.inputFilename = filename
            if verbose:
                self.replaceTextEdit(filename)
        except FileNotFoundError:
            self.writeErrorToLogs(
                "Error: No default input file found, check that config/default_trans.in exists.")
            return False
        except IOError:
            self.writeErrorToLogs("Error: No .xyz file selected to generate Plato input file.")
            return False
        except AssertionError:
            self.writeErrorToLogs(
                "Error: Insufficient terminals selected (min. two required). Select terminals by left clicking atoms.")
            return False
        if verbose:
            self.writeToLogs("Transmission input file " + self.inputFilename + ".in generated successfully.\n", "green")
            self.executeTransButton.setEnabled(True)
        return True

    def onGenerateCurrInputFileButtonClicked(self, boolean, verbose=True, bias=None, step_size=0.003):
        if bias is None:
            try:
                bias = float(self.biasLineEdit.text())
            except ValueError:
                self.writeErrorToLogs("Error: Missing input for bias.")
                return False
        try:
            reference_pot = float(self.referenceLineEdit.text())
        except ValueError:
            self.writeErrorToLogs("Error: Missing input for reference potential.")
            return
        try:
            excess = float(self.excessLineEdit.text())
        except ValueError:
            self.writeErrorToLogs("Error: Missing input for excess electrons.")
            return
        try:
            filename = curr_plato_input(self.openFileLineEdit.text(), self.transSelected, self.currentSelectedA,
                                        self.currentSelectedB, excess, reference_pot, bias, self.gammaLineEdit.text(),
                                        step_size, self.id)
            self.inputFilename = filename
            self.replaceTextEdit(filename)
        except FileNotFoundError:
            self.writeErrorToLogs(
                "Error: No default current input file found, check that config/default_curr.in exists.")
            return False
        except IOError:
            self.writeErrorToLogs("Error: No .xyz file selected to generate Plato input file.")
            return False
        except AssertionError:
            self.writeErrorToLogs(
                "Error: Insufficient terminals selected (two required). Select terminals by left clicking atoms.")
            return False
        except NotImplementedError:
            self.writeErrorToLogs(
                "Error: Incorrect number of terminals selected, may only calculate current between two terminals.")
            return False
        except ValueError:
            self.writeErrorToLogs(
                "Error: Insufficient atoms for region A (min. one required). Select atoms for A by right clicking.")
            return False
        except ZeroDivisionError:
            self.writeErrorToLogs(
                "Error: Insufficient atoms for region B (min. one required). Select atoms for B by middle clicking.")
            return False
        if verbose:
            self.writeToLogs("Current input file " + self.inputFilename + ".in generated successfully.\n", "green")
            self.executeCurrButton.setEnabled(True)
        return True

        # openFileButton
        # openFileLineEdit

    def onOpenFileButtonClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open xyz file',
                                                            filter="XYZ File (*.xyz);;All Files (*.*)")

        if filename:
            self.openFileLineEdit.setText(filename)

    def onOpenOutFileButtonClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open output file',
                                                            filter="Output File (*.out);;All Files (*.*)")

        if filename:
            self.openOutFileLineEdit.setText(filename)

    def onOpenWfFileButtonClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open wavefunction file',
                                                            filter="Wavefunction File (*.wf);;All Files (*.*)")
        if filename:
            self.openWfFileLineEdit.setText(filename)

    def onOpenCsvFileButtonClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open transmission csv file',
                                                            filter="CSV File (*.csv);;All Files (*.*)")

        if filename:
            self.openCsvFileLineEdit.setText(filename)

    def onOpenDirButtonClicked(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory(parent=self, caption='Select directory')

        if dirname:
            self.openDirLineEdit.setText(dirname)

    def onOpenDirGammaButtonClicked(self):
        dirname = QtWidgets.QFileDialog.getExistingDirectory(parent=self, caption='Select directory')

        if dirname:
            self.gammaOpenDirLineEdit.setText(dirname)

    def onExecuteLoadedButtonClicked(self):
        if self.openOutFileLineEdit.text() == "":
            self.writeErrorToLogs("Error: no Plato output file (.out) selected.")
            return
        if self.openWfFileLineEdit.text() == "":
            self.writeErrorToLogs("Error: no Plato wavefunction file (.wf) selected.")
            return
        self.atoms = input_file_setup(self.openOutFileLineEdit.text(), "config/attributes.txt",
                                      self.openWfFileLineEdit.text())
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(self.atoms[0].get_total_orbitals() - 1)
        self.openGLWidget.atoms = self.atoms
        self.draw()
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.mainDisplayTab))
        self.propertiesWindow.setCurrentIndex(self.propertiesWindow.indexOf(self.displaySettingsTab))
        self.writeToLogs("Execution carried out successfully.\n", "green")
        self.transSelected = {"1": [], "2": [], "3": [], "4": [], "5": []}
        self.currentSelectedA = []
        self.currentSelectedB = []

    def onTransExecuteLoadedButtonClicked(self):
        if self.openCsvFileLineEdit.text() == "":
            self.writeErrorToLogs("Error: no Plato generated csv file (.csv) selected.")
            return
        self.csvFilename = self.openCsvFileLineEdit.text()
        headers_mapped, headers = transmission_headers(self.csvFilename, self.transSelected)
        self.graphKeys = headers
        self.graphComboBox.clear()
        self.graphComboBox.addItems(headers_mapped)
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.graphTab))
        self.propertiesWindow.setCurrentIndex(self.propertiesWindow.indexOf(self.graphSettingsTab))
        self.writeToLogs("Graphs plotted successfully.\n", "green")

    def onCurrExecuteLoadedButtonClicked(self):
        if self.openDirLineEdit.text() == "":
            self.writeErrorToLogs("Error: no directory selected.")
            return
        bias_v, bias, currents = process_current_csv(self.openDirLineEdit.text())
        self.writeToLogs("Bias from directory determined to be " + bias_v + ".", "green")
        current_graph(self.graphWidget2, bias, currents)
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.graphTab2))
        self.writeToLogs("Current vs. bias graph plotted successfully.\n", "green")

    def onGammaExecuteLoadedButtonClicked(self):
        self.gammaGLWidget.clear()
        if self.gammaOpenDirLineEdit.text() == "":
            self.writeErrorToLogs("Error: no directory selected.")
            return
        energy, gamma, transmission = process_energy_gamma_trans_csv(self.gammaOpenDirLineEdit.text(), None)
        energy_gamma_trans_graph(self.gammaGLWidget, energy, gamma, transmission)
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.gammaGraphTab))
        self.propertiesWindow.setCurrentIndex(self.propertiesWindow.indexOf(self.graphSettingsTab))
        self.writeToLogs("Energy vs. gamma vs. transmission graph plotted successfully.\n", "green")

    # SwitchToInputFileTabButton

    def onSwitchToInputFileTabButtonClicked(self):
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.inputFileTab))

        # graphSettingsTab

    def setGraphComboBox(self):
        transmission_graph(self.graphWidget, self.csvFilename, self.graphKeys[self.graphComboBox.currentIndex()])

    def setTerminalComboBox(self):
        self.openGLWidget.terminal = self.terminalComboBox.currentIndex() + 1

        # atomSettingsTab
        # atomColSlider
        # atomColSliderLabel

    def setAtomColSliderLabel(self):
        value = self.atomColSlider.value()
        self.atomCol = value
        self.draw()

    def updateAtomColSliderLabel(self):
        value = self.atomColSlider.value()
        self.atomColSliderLabel.setText("Columns: " + str(value))

        # atomRowSlider
        # atomRowSliderLabel

    def setAtomRowSliderLabel(self):
        value = self.atomRowSlider.value()
        self.atomRow = value
        self.draw()

    def updateAtomRowSliderLabel(self):
        value = self.atomRowSlider.value()
        self.atomRowSliderLabel.setText("Rows: " + str(value))

        # bondColSlider
        # bondColSliderLabel

    def setBondColSliderLabel(self):
        value = self.bondColSlider.value()
        self.bondCol = value
        self.draw()

    def updateBondColSliderLabel(self):
        value = self.bondColSlider.value()
        self.bondColSliderLabel.setText("Columns: " + str(value))

        # bondRowSlider
        # bondRowSliderLabel

    def setBondRowSliderLabel(self):
        value = self.bondRowSlider.value()
        self.bondRow = value
        self.draw()

    def updateBondRowSliderLabel(self):
        value = self.bondRowSlider.value()
        self.bondRowSliderLabel.setText("Rows: " + str(value))

        # brightnessSlider
        # brightnessSliderLabel

    def setBrightnessSliderLabel(self):
        value = self.brightnessSlider.value()
        self.backgroundColor = (value, value, value)
        self.openGLWidget.setBackgroundColor(self.backgroundColor)

    def updateBrightnessSliderLabel(self):
        value = self.brightnessSlider.value()
        self.brightnessSliderLabel.setText("Brightness: " + str(value))

        # checkBoxIndex
        # checkBoxSymbol
        # checkBoxPosition
        # checkBoxRadius
        # fontComboBox
        # sizeComboBox
        # offsetComboBox
        # colourComboBox

    def setCheckBoxIndex(self, state):
        self.openGLWidget.index = state
        self.openGLWidget.update()

    def setCheckBoxSymbol(self, state):
        self.openGLWidget.symbol = state
        self.openGLWidget.update()

    def setCheckBoxPosition(self, state):
        self.openGLWidget.position = state
        self.openGLWidget.update()

    def setCheckBoxRadius(self, state):
        self.openGLWidget.radius = state
        self.openGLWidget.update()

    def setFontComboBox(self):
        self.openGLWidget.font = self.fontComboBox.currentText()
        self.openGLWidget.update()

    def setSizeComboBox(self):
        self.openGLWidget.size = int(self.sizeComboBox.currentText())
        self.openGLWidget.update()

    def setOffsetComboBox(self, state):
        self.openGLWidget.offset = state
        self.openGLWidget.update()

    def setColourComboBox(self):
        self.openGLWidget.colour = self.colourComboBox.currentText()
        self.openGLWidget.update()

        # bondRadiusSlider
        # bondRadiusSliderLabel

    def setBondRadiusSliderLabel(self):
        value = self.bondRadiusSlider.value()
        self.bondRadius = value / 100
        self.draw()

    def updateBondRadiusSliderLabel(self):
        value = self.bondRadiusSlider.value()
        self.bondRadiusSliderLabel.setText("Radius: " + str(value / 100))

        # bondThresholdSlider
        # bondThresholdSliderlabel

    def setBondThresholdSliderLabel(self):
        value = self.bondThresholdSlider.value()
        self.bondThreshold = value / 10
        self.draw()

    def updateBondThresholdSliderLabel(self):
        value = self.bondThresholdSlider.value()
        self.bondThresholdSliderLabel.setText("Length: " + str(value / 10))

        # switchToAttrFileTabButton

    def onSwitchToAttrFileTabButtonClicked(self):
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.attributeFileTab))

        # orbitalSettingsTab
        # advOrbWfCheckBox
        # advOrbHorzCheckBox
        # advOrbVertCheckBox
        # sphOrbWfCheckBox

    def draw(self):
        atoms_off = self.toggleAtomsButton.isChecked()
        self.openGLWidget.clear()

        # Plot atoms and bonds
        if not atoms_off:
            draw_atoms(self.atoms, self.openGLWidget, self.atomRow, self.atomCol)
            draw_bonds(self.atoms, self.openGLWidget, self.bondRow, self.bondCol, self.bondRadius, self.bondThreshold)
            draw_selection(self.atoms, self.openGLWidget, self.atomRow, self.atomCol)

        # Plot orbitals
        if self.advOrbWfCheckBox.isChecked():
            draw_advOrbWf(self.atoms, self.openGLWidget, self.mode, self.orbRow, self.orbCol, self.orbScaler,
                          self.theta, self.phi, self.R, self.G, self.B, self.A)

        if self.advOrbHorzCheckBox.isChecked():
            draw_advOrbHorz(self.atoms, self.openGLWidget, self.mode, self.orbScaler, self.R, self.G, self.B, self.A)

        if self.advOrbVertCheckBox.isChecked():
            draw_advOrbVert(self.atoms, self.openGLWidget, self.mode, self.orbScaler, self.R, self.G, self.B, self.A)

        if self.sphOrbWfCheckBox.isChecked():
            draw_sphOrbWf(self.atoms, self.openGLWidget, self.mode, self.orbRow, self.orbCol, self.orbScaler, self.R,
                          self.G, self.B, self.A)

        if self.sphOrbFacesCheckBox.isChecked():
            draw_sphOrbFaces(self.atoms, self.openGLWidget, self.mode, self.orbRow, self.orbCol, self.orbScaler, self.R,
                             self.G, self.B, self.A)

        if self.advOrbFacesCheckBox.isChecked():
            draw_advOrbFaces(self.atoms, self.openGLWidget, self.mode, self.orbRow, self.orbCol, self.orbScaler,
                             self.theta, self.phi, self.R, self.G, self.B, self.A)

        # orbColSlider
        # orbColSliderLabel

    def setOrbColSliderLabel(self):
        value = self.orbColSlider.value()
        self.orbCol = value
        self.draw()

    def updateOrbColSliderLabel(self):
        value = self.orbColSlider.value()
        self.orbColSliderLabel.setText("Columns: " + str(value))

        # orbRowSlider
        # orbRowSliderLabel

    def setOrbRowSliderLabel(self):
        value = self.orbRowSlider.value()
        self.orbRow = value
        self.draw()

    def updateOrbRowSliderLabel(self):
        value = self.orbRowSlider.value()
        self.orbRowSliderLabel.setText("Rows: " + str(value))

        # orbScalerSlider
        # orbScalerSliderLabel

    def setScalerSliderLabel(self):
        value = self.orbScalerSlider.value()
        self.orbScaler = value
        self.draw()

    def updateScalerSliderLabel(self):
        value = self.orbScalerSlider.value()
        self.orbScalerSliderLabel.setText("Scaler: " + str(value))

    def setThetaSliderLabel(self):
        value = self.thetaSlider.value()
        self.theta = math.radians(value)
        self.draw()

    def updateThetaSliderLabel(self):
        value = self.thetaSlider.value()
        self.thetaSliderLabel.setText("Theta: " + str(value))

    def setPhiSliderLabel(self):
        value = self.phiSlider.value()
        self.phi = math.radians(value)
        self.draw()

    def updatePhiSliderLabel(self):
        value = self.phiSlider.value()
        self.phiSliderLabel.setText("Phi: " + str(value))

    def setColourRSliderLabel(self):
        value = self.colourRSlider.value()
        self.R = value / 100
        self.draw()

    def setColourGSliderLabel(self):
        value = self.colourGSlider.value()
        self.G = value / 100
        self.draw()

    def setColourBSliderLabel(self):
        value = self.colourBSlider.value()
        self.B = value / 100
        self.draw()

    def setColourASliderLabel(self):
        value = self.colourASlider.value()
        self.A = value / 100
        self.draw()

    def updateColourRSliderLabel(self):
        value = self.colourRSlider.value()
        self.colourRSliderLabel.setText("R: " + str(value / 100))

    def updateColourGSliderLabel(self):
        value = self.colourGSlider.value()
        self.colourGSliderLabel.setText("G: " + str(value / 100))

    def updateColourBSliderLabel(self):
        value = self.colourBSlider.value()
        self.colourBSliderLabel.setText("B: " + str(value / 100))

    def updateColourASliderLabel(self):
        value = self.colourASlider.value()
        self.colourASliderLabel.setText("A: " + str(value / 100))

    # mainDisplayTab
    # horizontalSlider
    # horizontalSliderLabel
    def setHorizontalSliderLabel(self):
        value = self.horizontalSlider.value()
        self.mode = value
        self.draw()

    def updateHorizontalSliderLabel(self):
        value = self.horizontalSlider.value()
        self.horizontalSliderLabel.setText("Molecular Orbital: " + str(value + 1))
        self.horizontalSliderEnergyLabel.setText("Energy (eV): " + self.atoms[0].get_eigenenergy(value))

    # openGLWidget
    def onTransSelection(self):
        self.transSelected = {"1": [], "2": [], "3": [], "4": [], "5": []}
        self.draw()
        for i in range(len(self.atoms)):
            terminal = self.atoms[i].get_isSelectedTrans()
            if terminal:
                self.transSelected[str(terminal)].append(str(i + 1))
        self.writeToLogs("Selected atom indices for terminals 1-5:", "black")
        for key in self.transSelected:
            self.writeToLogs("Terminal " + key + ": " + ", ".join(self.transSelected[key]), colours(key))
        self.writeToLogs("\n", "black")

    def onCurrentSelectionA(self):
        self.currentSelectedA = []
        self.draw()
        for i in range(len(self.atoms)):
            if self.atoms[i].get_isSelectedCurrA():
                self.currentSelectedA.append(i + 1)
        if len(self.currentSelectedA) == 0:
            self.writeToLogs("No regions selected.", "purple")
            return
        selection = "Region A by atom index: "
        for j in range(len(self.currentSelectedA)):
            selection = selection + str(self.currentSelectedA[j]) + ", "
        self.writeToLogs(selection[:-2], "purple")

    def onCurrentSelectionB(self):
        self.currentSelectedB = []
        self.draw()
        for i in range(len(self.atoms)):
            if self.atoms[i].get_isSelectedCurrB():
                self.currentSelectedB.append(i + 1)
        if len(self.currentSelectedB) == 0:
            self.writeToLogs("No regions selected.", "lime")
            return
        selection = "Region B by atom index: "
        for j in range(len(self.currentSelectedB)):
            selection = selection + str(self.currentSelectedB[j]) + ", "
        self.writeToLogs(selection[:-2], "lime")

    # resetViewButton
    def onResetViewButtonClicked(self):
        self.openGLWidget.reset()
        self.openGLWidget.setBackgroundColor(self.backgroundColor)
        self.writeToLogs("View reset to default.", "grey")

    # saveImageButton
    def onSaveImageButtonClicked(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption='Save image',
                                                            filter="PNG Image (*.png);;JPEG Image (*.jpg);;All Files (*.*)")

        self.openGLWidget.readQImage().save(filename)

    def onSave3DImageButtonClicked(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption='Save image',
                                                            filter="PNG Image (*.png);;JPEG Image (*.jpg);;All Files (*.*)")

        self.gammaGLWidget.readQImage().save(filename)

    # toggleAtomsButton
    def onToggleAtomsButtonClicked(self):
        if self.toggleAtomsButton.isChecked():
            self.draw()
            self.writeToLogs("Atoms toggled off.", "grey")
            return
        self.draw()
        self.writeToLogs("Atoms toggled on.", "grey")

    # inputFileTab
    # inputTextEdit
    # saveInputFileButton
    def onSaveInputFileButtonClicked(self):
        with open(self.inputFilename + ".in", 'w') as f:
            f.write(str(self.inputTextEdit.toPlainText()))
        self.writeToLogs("Input file " + self.inputFilename + ".in saved successfully.", "green")

    def onGammaLineEditChanged(self):
        string = self.gammaLineEdit.text()
        if not isposfloat(string):
            self.writeErrorToLogs("Error: non-positive float '" + string + "' entered for gamma.")
            self.gammaLineEdit.setText("")
            self.gammaLineEdit2.setText("")
        else:
            self.gammaLineEdit.setText(string)
            self.gammaLineEdit2.setText(string)

    def onGammaLineEditChanged2(self):
        string = self.gammaLineEdit2.text()
        if not isposfloat(string):
            self.writeErrorToLogs("Error: non-positive float '" + string + "' entered for gamma.")
            self.gammaLineEdit.setText("")
            self.gammaLineEdit2.setText("")
        else:
            self.gammaLineEdit.setText(string)
            self.gammaLineEdit2.setText(string)

    def onExcessLineEditChanged(self):
        string = self.excessLineEdit.text()
        if not isfloat(string):
            self.writeErrorToLogs("Error: non-float '" + string + "' entered for excess electrons.")
            self.excessLineEdit.setText("")

    def onReferenceLineEditChanged(self):
        string = self.referenceLineEdit.text()
        if not isfloat(string):
            self.writeErrorToLogs("Error: non-float '" + string + "' entered for reference potential.")
            self.referenceLineEdit.setText("")

    def onBiasLineEditChanged(self):
        string = self.biasLineEdit.text()
        if not isfloat(string):
            self.writeErrorToLogs("Error: non-float '" + string + "' entered for bias.")
            self.biasLineEdit.setText("")

    def onStepsLineEditChanged(self):
        string = self.stepsLineEdit.text()
        if not isnatnumber(string):
            self.writeErrorToLogs("Error: non-natural number '" + string + "' entered for steps.")
            self.stepsLineEdit.setText("")

    def onGammaStartLineEditChanged(self):
        string = self.gammaStartLineEdit.text()
        if not isposfloat(string):
            self.writeErrorToLogs("Error: non-pos float '" + string + "' entered for gamma start value.")
            self.gammaStartLineEdit.setText("")

    def onGammaEndLineEditChanged(self):
        string = self.gammaEndLineEdit.text()
        if not isposfloat(string):
            self.writeErrorToLogs("Error: non-pos float '" + string + "' entered for gamma end value.")
            self.gammaEndLineEdit.setText("")

    def onGammaStepsLineEditChanged(self):
        string = self.gammaStepsLineEdit.text()
        if not isnatnumber(string):
            self.writeErrorToLogs("Error: non-natural number '" + string + "' entered for gamma steps value.")
            self.gammaStepsLineEdit.setText("")

    # AttributeFileTab
    # attributeTextEdit
    # saveAttributeFileButton
    def onSaveAttributeFileButtonClicked(self):
        with open("config/attributes.txt", 'w') as f:
            f.write(str(self.attributeTextEdit.toPlainText()))
        self.writeToLogs("Attribute file attributes.txt modified successfully. Settings will be applied on next "
                         "execution", "green")

    # fullConsoleTab
    # fullConsoleTextEdit
    def writeToLogs(self, text, color):
        self.consoleLog.setTextColor(QColor(color))
        self.fullConsoleLog.setTextColor(QColor(color))
        self.consoleLog.append(text)
        self.fullConsoleLog.append(text)

    def writeErrorToLogs(self, text):
        self.consoleLog.setTextColor(QColor("red"))
        self.fullConsoleLog.setTextColor(QColor("red"))
        self.consoleLog.append(text)
        self.fullConsoleLog.append(text)
        self.fullConsoleLog.append(traceback.format_exc())


if __name__ == '__main__':
    main = MainWindow(resolution.width)
    # main = MainWindow(resolution.width, default_input)
    main.show()
    sys.exit(app.exec_())
