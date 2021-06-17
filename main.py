from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon, QColor

from atom import Atom
from plot import *
from input import input_file_setup, xyz_to_plato_input, trans_plato_input, curr_plato_input, find_current_in_file, isfloat, isdigit
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
# default_input = input_file_setup("config/benzene.out", "config/attributes.txt", "config/benzene.wf")


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
        self.inputFilename = None
        self.transInputFilename = None
        self.currInputFilename = None
        self.transSelected = []
        self.currentSelectedA = []
        self.currentSelectedB = []
        self.mode = 0

        ###### Initialise propertiesWindow ######
        ### setupSettingsTab
        # executeButton
        self.executeButton.clicked.connect(self.onExecuteButtonClicked)

        # executeTransButton
        self.executeTransButton.clicked.connect(self.onTransExecuteButtonClicked)

        # executeCurrButton and executeCurrGraphButton
        self.executeCurrButton.clicked.connect(self.onExecuteCurrButtonClicked)
        self.executeCurrGraphButton.clicked.connect(self.onExecuteCurrGraphButtonClicked)

        # executeLoadedButton and transExecuteLoadedButton
        self.executeLoadedButton.clicked.connect(self.onExecuteLoadedButtonClicked)
        self.transExecuteLoadedButton.clicked.connect(self.onTransExecuteLoadedButtonClicked)

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
        self.sizeComboBox.addItems(["12", "14", "16", "18", "20", "24", "30", "42"])
        self.offsetComboBox.addItems(["X", "Y", "Z"])
        self.colourComboBox.addItems(["Red", "Lime", "Blue", "Purple", "Orange", "Yellow"])
        self.openGLWidget.font = "Arial"
        self.openGLWidget.size = 12
        self.openGLWidget.offset = 0
        self.openGLWidget.colour = "Red"

        ### graphSettingsTab
        self.graphComboBox.currentIndexChanged.connect(self.setGraphComboBox)

        ### atomSettingsTab
        # atomColSlider
        self.atomCol = self.atomColSlider.value()
        # atomColSliderLabel
        self.atomColSlider.valueChanged.connect(self.setAtomColSliderLabel)

        # atomRowSlider
        self.atomRow = self.atomRowSlider.value()
        # atomRowSliderLabel
        self.atomRowSlider.valueChanged.connect(self.setAtomRowSliderLabel)

        # bondColSlider
        self.bondCol = self.bondColSlider.value()
        # bondColSliderLabel
        self.bondColSlider.valueChanged.connect(self.setBondColSliderLabel)

        # bondRowSlider
        self.bondRow = self.bondRowSlider.value()
        # bondRowSliderLabel
        self.bondRowSlider.valueChanged.connect(self.setBondRowSliderLabel)

        # brightnessSlider
        # brightnessSliderLabel
        self.brightnessSlider.valueChanged.connect(self.setBrightnessSliderLabel)

        # bondRadiusSlider
        self.bondRadius = 0.15
        # bondRadiusSliderLabel
        self.bondRadiusSlider.valueChanged.connect(self.setBondRadiusSliderLabel)

        # bondThresholdSlider
        self.bondThreshold = 3.0
        # bondThersholdSliderlabel
        self.bondThresholdSlider.valueChanged.connect(self.setBondThresholdSliderLabel)

        # switchToAttrFileTabButton
        self.switchToAttrFileTabButton.clicked.connect(self.onSwitchToAttrFileTabButtonClicked)

        ### orbitalSettingsTab
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
        self.orbColSlider.valueChanged.connect(self.setOrbColSliderLabel)

        # orbRowSlider
        self.orbRow = self.orbRowSlider.value()
        # orbRowSliderLabel
        self.orbRowSlider.valueChanged.connect(self.setOrbRowSliderLabel)

        # orbScalerSlider
        self.orbScaler = self.orbScalerSlider.value()
        # orbScalerSliderLabel
        self.orbScalerSlider.valueChanged.connect(self.setScalerSliderLabel)

        # thetaSlider
        self.theta = self.thetaSlider.value()
        # thetaSliderLabel
        self.thetaSlider.valueChanged.connect(self.setThetaSliderLabel)

        # phiSlider
        self.phi = math.radians(self.phiSlider.value())
        # phiSliderLabel
        self.phiSlider.valueChanged.connect(self.setPhiSliderLabel)

        # colourXSlider
        self.R = 1.00
        self.G = 0.00
        self.B = 1.00
        self.A = 0.50
        self.colourRSlider.valueChanged.connect(self.setColourRSliderLabel)
        self.colourGSlider.valueChanged.connect(self.setColourGSliderLabel)
        self.colourBSlider.valueChanged.connect(self.setColourBSliderLabel)
        self.colourASlider.valueChanged.connect(self.setColourASliderLabel)

        ###### Initialise mainWindow ######

        ### mainDisplayTab
        # horizontalSlider
        # horizontalSliderLabel
        self.horizontalSlider.valueChanged.connect(self.setHorizontalSliderLabel)

        # openGLWidget
        self.openGLWidget.opts['distance'] = 15
        self.openGLWidget.multiplier = self.multiplier
        self.openGLWidget.atoms = [
            Atom("0", 0, -7, 0, "Welcome to Platomic. To get started, select an .xyz file in the 'Plato setup' tab."),
            Atom("0", 0, -7.25, -1, "Hover over any (?) icons for help and / or additional information."),
            Atom("0", 0, -7.5, -2, "For a full in-depth tutorial check out the User Guide.")]
        # self.openGLWidget.atoms = self.atoms
        self.backgroundColor = (40, 40, 40)
        self.openGLWidget.setBackgroundColor(self.backgroundColor)
        self.openGLWidget.left_clicked.connect(self.onTransSelection)
        self.openGLWidget.middle_clicked.connect(self.onCurrentSelectionA)
        self.openGLWidget.right_clicked.connect(self.onCurrentSelectionB)
        # self.draw()

        # resetViewButton
        self.resetViewButton.clicked.connect(self.onResetViewButtonClicked)

        # saveImageButton
        self.saveImageButton.clicked.connect(self.onSaveImageButtonClicked)

        # toggleAtomsButton
        self.toggleAtomsButton.clicked.connect(self.onToggleAtomsButtonClicked)

        ### inputFileTab
        # inputTextEdit
        # saveInputFileButton
        self.saveInputFileButton.clicked.connect(self.onSaveInputFileButtonClicked)

        ### AttributeFileTab
        # attributeTextEdit
        with open("config/attributes.txt", "r") as f:
            contents = f.readlines()
        for line, content in enumerate(contents):
            self.attributeTextEdit.insertPlainText(content)

        # saveAttributeFileButton
        self.saveAttributeFileButton.clicked.connect(self.onSaveAttributeFileButtonClicked)

        ### fullConsoleTab
        # fullConsoleTextEdit

    ###### Initialise functions ######
    ###### Initialise propertiesWindow ######
    ### setupSettingsTab
    # executeButton
    def onExecuteButtonClicked(self):
        if os.name == 'nt':
            self.writeErrorToLogs("Plato back-end execution is not supported on Windows systems.")
            return
        try:
            command = "(cd ./Plato/bin && ./tb1 ../../" + self.inputFilename + ")"
        except TypeError:
            self.writeErrorToLogs("No Plato input file found, click generate before clicking execute.")
            return
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if result.returncode:
            self.writeToLogs(result.stderr, "red")
            if result.stdout:
                self.writeToLogs(result.stdout, "red")
            return
        if result.stdout:
            self.writeToLogs(result.stdout, "black")
        self.atoms = input_file_setup(self.inputFilename + ".out", "config/attributes.txt", self.inputFilename + ".wf")
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(self.atoms[0].get_total_orbitals() - 1)
        self.openGLWidget.atoms = self.atoms
        self.draw()
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.mainDisplayTab))
        self.writeToLogs("Execution carried out successfully.", "green")
        self.transSelected = []
        self.currentSelectedA = []
        self.currentSelectedB = []

    def onTransExecuteButtonClicked(self):
        if os.name == 'nt':
            self.writeErrorToLogs("Plato back-end execution is not supported on Windows systems.")
            return
        try:
            command = "(cd ./Plato/bin && ./tb1 ../../" + self.inputFilename + ")"
        except TypeError:
            self.writeErrorToLogs("No Plato input file found, click generate before clicking execute.")
            return
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if result.returncode:
            self.writeToLogs(result.stderr, "red")
            if result.stdout:
                self.writeToLogs(result.stdout, "red")
            return
        if result.stdout:
            self.writeToLogs(result.stdout, "black")
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.graphTab))
        self.writeToLogs("Execution carried out successfully.", "green")
        headers = transmission_graph(self.graphWidget, self.inputFilename + "_trans.csv")
        self.graphComboBox.addItems(headers)
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.graphTab))
        self.writeToLogs("Graphs plotted successfully.", "green")

    def onExecuteCurrButtonClicked(self):
        if os.name == 'nt':
            self.writeErrorToLogs("Plato back-end execution is not supported on Windows systems.")
            return
        try:
            command = "(cd ./Plato/bin && ./tb1 ../../" + self.inputFilename + ")"
        except TypeError:
            self.writeErrorToLogs("No Plato input file found, click generate before clicking execute.")
            return
        result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
        if result.returncode:
            self.writeToLogs(result.stderr, "red")
            if result.stdout:
                self.writeToLogs(result.stdout, "red")
            return
        if result.stdout:
            self.writeToLogs(result.stdout, "black")
        self.writeToLogs("Execution carried out successfully.", "green")
        current = find_current_in_file(self.inputFilename + ".out")
        self.writeToLogs("Current: " + current + " mA.", "green")
        return float(current)

    def onExecuteCurrGraphButtonClicked(self):
        if not len(self.transSelected) == 2:
            self.writeErrorToLogs(
                "Error: two terminals should be selected for current vs. bias graphs. Select terminals by left clicking atoms.")
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
        array = np.linspace(0, float(self.biasLineEdit.text()), int(self.stepsLineEdit.text()))
        for i in array:
            bias = round(i, 4)
            self.onGenerateCurrInputFileButtonClicked(bias=bias, current_calc=True)
            currents.append(self.onExecuteCurrButtonClicked())
        current_graph(self.graphWidget2, array, currents)
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.graphTab2))
        self.writeToLogs("Current vs. bias graphs plotted successfully.", "green")

    # generateInputFileButton

    def onGenerateInputFileButtonClicked(self):
        self.inputTextEdit.clear()
        try:
            filename = xyz_to_plato_input(self.openFileLineEdit.text())
            self.inputFilename = filename
            with open(filename + ".in", "r") as f:
                contents = f.readlines()
            for line, content in enumerate(contents):
                self.inputTextEdit.insertPlainText(content)
        except FileNotFoundError:
            self.writeErrorToLogs("Error: No default input file found, check that config/default.in exists.")
            return
        except IOError:
            self.writeErrorToLogs("Error: No .xyz file selected to generate Plato input file.")
            return
        self.writeToLogs("Input file " + self.inputFilename + ".in generated successfully.", "green")

    def onGenerateTransInputFileButtonClicked(self):
        self.inputTextEdit.clear()
        try:
            filename = trans_plato_input(self.openFileLineEdit.text(), self.transSelected)
            self.inputFilename = filename
            with open(filename + ".in", "r") as f:
                contents = f.readlines()
            for line, content in enumerate(contents):
                self.inputTextEdit.insertPlainText(content)
        except FileNotFoundError:
            self.writeErrorToLogs(
                "Error: No default input file found, check that config/default_trans.in exists.")
            return
        except IOError:
            self.writeErrorToLogs("Error: No .xyz file selected to generate Plato input file.")
            return
        except AssertionError:
            self.writeErrorToLogs(
                "Error: Insufficient terminals selected (min. two required). Select terminals by left clicking atoms.")
            return
        self.writeToLogs("Transmission input file " + self.inputFilename + ".in generated successfully.", "green")

    def onGenerateCurrInputFileButtonClicked(self, reference_pot=0, bias=0, gamma=0.1, current_calc=False):
        self.inputTextEdit.clear()
        try:
            filename = curr_plato_input(self.openFileLineEdit.text(), self.transSelected, self.currentSelectedA,
                                        self.currentSelectedB, reference_pot, bias, gamma, current_calc)
            self.inputFilename = filename
            with open(filename + ".in", "r") as f:
                contents = f.readlines()
            for line, content in enumerate(contents):
                self.inputTextEdit.insertPlainText(content)
        except AssertionError:
            self.writeErrorToLogs(
                "Error: Insufficient terminals selected (min. two required). Select terminals by left clicking atoms.")
            return
        except ValueError:
            self.writeErrorToLogs(
                "Error: Insufficient atoms for region A (min. one required). Select atoms for A by middle clicking.")
            return
        except ZeroDivisionError:
            self.writeErrorToLogs(
                "Error: Insufficient atoms for region B (min. one required). Select atoms for B by middle clicking.")
            return
        except FileNotFoundError:
            self.writeErrorToLogs(
                "Error: No default current input file found, check that config/default_curr.in exists.")
            return
        except IOError:
            self.writeErrorToLogs("Error: No .xyz file selected to generate Plato input file.")
            return

        self.writeToLogs("Current input file " + self.inputFilename + ".in generated successfully.", "green")

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

    def onExecuteLoadedButtonClicked(self):
        self.atoms = input_file_setup(self.openOutFileLineEdit.text(), "config/attributes.txt",
                                      self.openWfFileLineEdit.text())
        self.openGLWidget.atoms = self.atoms
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(self.atoms[0].get_total_orbitals() - 1)
        self.draw()
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.mainDisplayTab))
        self.writeToLogs("Execution carried out successfully.", "green")

    def onTransExecuteLoadedButtonClicked(self):
        headers = transmission_graph(self.graphWidget, self.openCsvFileLineEdit.text())
        self.graphComboBox.addItems(headers)
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.graphTab))
        self.writeToLogs("Graphs plotted successfully.", "green")

    # SwitchToInputFileTabButton

    def onSwitchToInputFileTabButtonClicked(self):
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.inputFileTab))

        # SwitchToTransInputFileTabButton

    def onSwitchToTransInputFileTabButtonClicked(self):
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.transInputFileTab))

        ### graphSettingsTab

    def setGraphComboBox(self):
        if self.inputFilename is None:
            filename = self.openCsvFileLineEdit.text()
        else:
            filename = self.inputFilename + ".csv"
        # transmission_graph2(self.graphWidget, filename, self.graphComboBox.currentText(), self.atoms[0].get_eigenenergies())

        ### atomSettingsTab
        # atomColSlider
        # atomColSliderLabel

    def setAtomColSliderLabel(self, value):
        self.atomCol = value
        self.draw()
        self.atomColSliderLabel.setText("Columns: " + str(value))

        # atomRowSlider
        # atomRowSliderLabel

    def setAtomRowSliderLabel(self, value):
        self.atomRow = value
        self.draw()
        self.atomRowSliderLabel.setText("Rows: " + str(value))

        # bondColSlider
        # bondColSliderLabel

    def setBondColSliderLabel(self, value):
        self.bondCol = value
        self.draw()
        self.bondColSliderLabel.setText("Columns: " + str(value))

        # bondRowSlider
        # bondRowSliderLabel

    def setBondRowSliderLabel(self, value):
        self.bondRow = value
        self.draw()
        self.bondRowSliderLabel.setText("Rows: " + str(value))

        # brightnessSlider
        # brightnessSliderLabel

    def setBrightnessSliderLabel(self, value):
        self.backgroundColor = (value, value, value)
        self.openGLWidget.setBackgroundColor(self.backgroundColor)
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

    def setFontComboBox(self, state):
        self.openGLWidget.font = self.fontComboBox.currentText()
        self.openGLWidget.update()

    def setSizeComboBox(self, state):
        self.openGLWidget.size = int(self.sizeComboBox.currentText())
        self.openGLWidget.update()

    def setOffsetComboBox(self, state):
        self.openGLWidget.offset = state
        self.openGLWidget.update()

    def setColourComboBox(self, state):
        self.openGLWidget.colour = self.colourComboBox.currentText()
        self.openGLWidget.update()

        # bondRadiusSlider
        # bondRadiusSliderLabel

    def setBondRadiusSliderLabel(self, value):
        self.bondRadius = value / 100
        self.draw()
        self.bondRadiusSliderLabel.setText("Radius: " + str(value / 100))

        # bondThresholdSlider
        # bondThresholdSliderlabel

    def setBondThresholdSliderLabel(self, value):
        self.bondThreshold = value / 10
        self.draw()
        self.bondThresholdSliderLabel.setText("Length: " + str(value / 10))

        # switchToAttrFileTabButton

    def onSwitchToAttrFileTabButtonClicked(self):
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.attributeFileTab))

        ### orbitalSettingsTab
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

    def setOrbColSliderLabel(self, value):
        self.orbCol = value
        self.draw()
        self.orbColSliderLabel.setText("Columns: " + str(value))

        # orbRowSlider
        # orbRowSliderLabel

    def setOrbRowSliderLabel(self, value):
        self.orbRow = value
        self.draw()
        self.orbRowSliderLabel.setText("Rows: " + str(value))

        # orbScalerSlider
        # orbScalerSliderLabel

    def setScalerSliderLabel(self, value):
        self.orbScaler = value
        self.draw()
        self.orbScalerSliderLabel.setText("Scaler: " + str(value))

    def setThetaSliderLabel(self, value):
        self.theta = math.radians(value)
        self.draw()
        self.thetaSliderLabel.setText("Theta: " + str(value))

    def setPhiSliderLabel(self, value):
        self.phi = math.radians(value)
        self.draw()
        self.phiSliderLabel.setText("Phi: " + str(value))

    def setColourRSliderLabel(self, value):
        self.R = value / 100
        self.draw()
        self.colourRSliderLabel.setText("R: " + str(value / 100))

    def setColourGSliderLabel(self, value):
        self.G = value / 100
        self.draw()
        self.colourGSliderLabel.setText("G: " + str(value / 100))

    def setColourBSliderLabel(self, value):
        self.B = value / 100
        self.draw()
        self.colourBSliderLabel.setText("B: " + str(value / 100))

    def setColourASliderLabel(self, value):
        self.A = value / 100
        self.draw()
        self.colourASliderLabel.setText("A: " + str(value / 100))

    ### mainDisplayTab
    # horizontalSlider
    # horizontalSliderLabel
    def setHorizontalSliderLabel(self, value):
        self.mode = value
        self.draw()
        self.horizontalSliderLabel.setText("MO: " + str(value + 1))
        self.horizontalSliderEnergyLabel.setText("Energy (eV): " + self.atoms[0].get_eigenenergy(value))

    # openGLWidget
    def onTransSelection(self):
        self.transSelected = []
        self.draw()
        for i in range(len(self.atoms)):
            if self.atoms[i].get_isSelectedTrans():
                self.transSelected.append(i + 1)
        if len(self.transSelected) == 0:
            self.writeToLogs("No terminals selected.", "orange")
            return
        selection = "Selected terminals by atom index: "
        for j in range(len(self.transSelected)):
            selection = selection + str(self.transSelected[j]) + ", "
        self.writeToLogs(selection[:-2], "orange")
        self.openGLWidget.update()

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
        self.openGLWidget.update()

    def onCurrentSelectionB(self):
        self.currentSelectedB = []
        self.draw()
        for i in range(len(self.atoms)):
            if self.atoms[i].get_isSelectedCurrB():
                self.currentSelectedB.append(i + 1)
        if len(self.currentSelectedB) == 0:
            self.writeToLogs("No regions selected.", "green")
            return
        selection = "Region B by atom index: "
        for j in range(len(self.currentSelectedB)):
            selection = selection + str(self.currentSelectedB[j]) + ", "
        self.writeToLogs(selection[:-2], "green")
        self.openGLWidget.update()

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

    # toggleAtomsButton
    def onToggleAtomsButtonClicked(self):
        if self.toggleAtomsButton.isChecked():
            self.draw()
            self.writeToLogs("Atoms toggled off.", "grey")
            return
        self.draw()
        self.writeToLogs("Atoms toggled on.", "grey")

    ### inputFileTab
    # inputTextEdit
    # saveInputFileButton
    def onSaveInputFileButtonClicked(self):
        with open(self.inputFilename + ".in", 'w') as f:
            f.write(str(self.inputTextEdit.toPlainText()))
        self.writeToLogs("Input file " + self.inputFilename + ".in saved successfully.", "green")

    def onReferenceLineEditChanged(self):
        string = self.referenceLineEdit.text()
        if not isfloat(string):
            self.writeErrorToLogs("Error: invalid number '" + string + "' entered for reference potential.")
            self.referenceLineEdit.setText("")

    def onBiasLineEditChanged(self):
        string = self.biasLineEdit.text()
        if not isfloat(string):
            self.writeErrorToLogs("Error: invalid number '" + string + "' entered for bias.")
            self.biasLineEdit.setText("")

    def onStepsLineEditChanged(self):
        string = self.stepsLineEdit.text()
        if not isdigit(string):
            self.writeErrorToLogs("Error: invalid number '" + string + "' entered for steps.")
            self.stepsLineEdit.setText("")

    ### AttributeFileTab
    # attributeTextEdit
    # saveAttributeFileButton
    def onSaveAttributeFileButtonClicked(self):
        with open("config/attributes.txt", 'w') as f:
            f.write(str(self.attributeTextEdit.toPlainText()))
        self.writeToLogs("Attribute file attributes.txt modified successfully. Settings will be applied on next "
                         "execution", "green")

    ### fullConsoleTab
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
