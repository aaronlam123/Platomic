from PyQt5 import QtWidgets, QtGui, uic
from plot import *
from input import input_file_setup, xyz_to_plato_input
from custom import scaledQImage
from subprocess import PIPE, run
import math
import os
import numpy as np
import sys
import pyautogui
import traceback

np.seterr(divide='ignore', invalid='ignore')


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, atoms, screen_width, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Load the UI Page
        uic.loadUi('config/mainwindow5.ui', self)
        self.setWindowTitle('Platomic')
        self.setWindowIcon(QtGui.QIcon("config/platomic.png"))
        self.multiplier = int(screen_width / 1920)

        # Initialise state
        self.atoms = atoms
        self.inputFilename = None
        self.mode = 0

        ###### Initialise propertiesWindow ######
        ### setupSettingsTab
        # executeButton
        self.executeButton.clicked.connect(self.onExecuteButtonClicked)

        # generateInputFileButton
        self.generateInputFileButton.clicked.connect(self.onGenerateInputFileButtonClicked)

        # openFileButton
        self.openFileButton.clicked.connect(self.onOpenFileButtonClicked)

        # openFileLineEdit

        # SwitchToInputFileTabButton
        self.switchToInputFileTabButton.clicked.connect(self.onSwitchToInputFileTabButtonClicked)

        ### atomSettingsTab
        # atomColSlider
        self.atomCol = 20
        # atomColSliderLabel
        self.atomColSlider.valueChanged.connect(self.setAtomColSliderLabel)

        # atomRowSlider
        self.atomRow = 10
        # atomRowSliderLabel
        self.atomRowSlider.valueChanged.connect(self.setAtomRowSliderLabel)

        # bondColSlider
        self.bondCol = 10
        # bondColSliderLabel
        self.bondColSlider.valueChanged.connect(self.setBondColSliderLabel)

        # bondRowSlider
        self.bondRow = 5
        # bondRowSliderLabel
        self.bondRowSlider.valueChanged.connect(self.setBondRowSliderLabel)

        # brightnessSlider
        # brightnessSliderLabel
        self.brightnessSlider.valueChanged.connect(self.setBrightnessSliderLabel)

        # bondRadiusSlider
        self.bondRadius = 0.1
        # bondRadiusSliderLabel
        self.bondRadiusSlider.valueChanged.connect(self.setBondRadiusSliderLabel)

        # bondThresholdSlider
        self.bondThreshold = 3
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
        self.orbCol = 20
        # orbColSliderLabel
        self.orbColSlider.valueChanged.connect(self.setOrbColSliderLabel)

        # orbRowSlider
        self.orbRow = 20
        # orbRowSliderLabel
        self.orbRowSlider.valueChanged.connect(self.setOrbRowSliderLabel)

        # orbScalerSlider
        self.orbScaler = 8
        # orbScalerSliderLabel
        self.orbScalerSlider.valueChanged.connect(self.setScalerSliderLabel)

        # thetaSlider
        self.theta = 0
        # thetaSliderLabel
        self.thetaSlider.valueChanged.connect(self.setThetaSliderLabel)

        # phiSlider
        self.phi = 0
        # phiSliderLabel
        self.phiSlider.valueChanged.connect(self.setPhiSliderLabel)

        # colourXSlider
        self.R = 1.00
        self.G = 0.00
        self.B = 1.00
        self.A = 1.00
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
        self.backgroundColor = (40, 40, 40)
        self.openGLWidget.setBackgroundColor(self.backgroundColor)
        self.draw()

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
        try:
            command = "(cd ./Plato/bin && ./tb1 ../../" + self.inputFilename + ")"
        except TypeError:
            self.writeErrorToLogs("No Plato input file found, click generate before clicking execute.")
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
        self.draw()
        self.writeToLogs("Execution carried out successfully.", "green")

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
        except IOError:
            self.writeErrorToLogs("Error: No .xyz file selected to generate Plato input file.")
        self.writeToLogs("Input file " + self.inputFilename + ".in generated successfully.", "green")

        # openFileButton
        # openFileLineEdit

    def onOpenFileButtonClicked(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open file',
                                                            filter="XYZ File (*.xyz);;All Files (*.*)")

        if filename:
            self.openFileLineEdit.setText(filename)

        # SwitchToInputFileTabButton

    def onSwitchToInputFileTabButtonClicked(self):
        self.mainWindow.setCurrentIndex(self.mainWindow.indexOf(self.inputFileTab))

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
        self.horizontalSliderLabel.setText("Mode: " + str(value + 1))

    # openGLWidget

    # resetViewButton
    def onResetViewButtonClicked(self):
        self.openGLWidget.reset()
        self.openGLWidget.setBackgroundColor(self.backgroundColor)
        self.writeToLogs("View reset to default.", "grey")

    # saveImageButton
    def onSaveImageButtonClicked(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(parent=self, caption='Save image',
                                                            filter="PNG Image (*.png);;JPEG Image (*.jpg);;All Files (*.*)")

        scaledQImage(self.openGLWidget, self.multiplier).save(filename)

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
        self.consoleLog.setTextColor(QtGui.QColor(color))
        self.fullConsoleLog.setTextColor(QtGui.QColor(color))
        self.consoleLog.append(text)
        self.fullConsoleLog.append(text)

    def writeErrorToLogs(self, text):
        self.consoleLog.setTextColor(QtGui.QColor("red"))
        self.fullConsoleLog.setTextColor(QtGui.QColor("red"))
        self.consoleLog.append(text)
        self.fullConsoleLog.append(text)
        self.fullConsoleLog.append(traceback.format_exc())


if __name__ == '__main__':
    resolution = pyautogui.size()
    # print(resolution)
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    # QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    app = QtWidgets.QApplication(sys.argv)
    # screen = app.primaryScreen()
    # print('Screen: %s' % screen.name())
    # size = screen.size()
    # print('Size: %d x %d' % (size.width(), size.height()))

    default_input = input_file_setup("config/benzene.out", "config/attributes.txt", "config/benzene.wf")
    main = MainWindow(default_input, resolution.width)
    main.show()
    sys.exit(app.exec_())
