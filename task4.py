import math
import numpy as np
from matplotlib import pyplot as plt
from style.gui import CenteredTextLabel
from test_scripts.task4_signalcompare import *
from test_scripts.task1_comparesignals import SignalSamplesAreEqual


# self.isPeriodic=0  =>>    self.firstCoulmn=Index,            self.secondCoulmn = Frequency
# self.isPeriodic=1  =>>    self.firstCoulmn=SampleAmplitude,  self.secondCoulmn = PhaseShift

class Task4:
  def __init__(self, dsp_class, gui):
    self.dsp_class = dsp_class
    self.gui = gui
    self.setupTask()

  def setupTask(self):
    self.gui.p1_t4_flineEdit_fileName.setPlaceholderText("Enter file name")
    self.clearTable()
    self.isPeriodic = -1
    self.complexList = []
    self.gui.p1_t4_btn_openFile.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t4_flineEdit_filePath))  # connect button to open file to read signal
    self.gui.p1_t4_btn_generateTable.clicked.connect(lambda: self.generate_table_from_file(self.gui.p1_t4_flineEdit_filePath.text()))
    self.gui.p1_t4_btn_clearTable.clicked.connect(self.clearTable)
    self.gui.p1_t4_btn_DFT.clicked.connect(self.DFT)
    self.gui.p1_t4_btn_IDFT.clicked.connect(self.IDFT)
    self.gui.p1_t4_f2_btn_generateTable.clicked.connect(self.editOnsampleData)
    self.gui.p1_t4_btn_saveTextFile.clicked.connect(self.save_in_file)
    self.gui.p1_t4_f1_btn_generateGraph.clicked.connect(self.generate_graphData)
    print('Task 4 Build Successfully')

  def clearTable(self):
    self.gui.p1_t4_tableWidget.clear()
    self.gui.p1_t4_tableWidget.setRowCount(0)
    self.gui.p1_t4_f1.setEnabled(False)
    self.gui.p1_t4_f2.setEnabled(False)
    self.gui.p1_t4_btn_saveTextFile.setEnabled(False)
    self.gui.p1_t4_btn_DFT.setEnabled(False)
    self.gui.p1_t4_btn_IDFT.setEnabled(False)
    self.gui.p1_t4_f2_flineEdit_sampleNumber.setText("")
    self.gui.p1_t4_f2_flineEdit_amplitude.setText("")
    self.gui.p1_t4_f2_flineEdit_phaseShift.setText("")
    self.gui.p1_t4_f1_flineEdit_sampleFreq.setText("")

  def generate_table_from_file(self, filePath):
    if len(filePath) == 0:
      self.gui.p1_label_result.setText("Error: Please Choose Signal File")
      return

    signalType, isPeriodic, N1, firstCoulmn, secondCoulmn = self.dsp_class.readData(filePath)
    self.signalType = signalType
    self.isPeriodic = isPeriodic
    self.N1 = N1
    self.firstCoulmn = firstCoulmn
    self.secondCoulmn = secondCoulmn
    self.fill_table()

  def fill_table(self):
    self.clearTable()
    self.check_status()
    self.gui.p1_t4_btn_saveTextFile.setEnabled(True)
    if self.isPeriodic==0:
      self.gui.p1_t4_tableWidget.setHorizontalHeaderLabels(('Index', 'Frequency'))
    elif self.isPeriodic==1:
      self.gui.p1_t4_tableWidget.setHorizontalHeaderLabels(('Amplitude', 'Phase Shift'))

    self.gui.p1_t4_tableWidget.setRowCount(self.N1)
    for i in range(self.N1):
      self.gui.p1_t4_tableWidget.setCellWidget(i, 0, CenteredTextLabel( str(self.firstCoulmn[i]) ))
      self.gui.p1_t4_tableWidget.setCellWidget(i, 1, CenteredTextLabel( str(self.secondCoulmn[i]) ))

  def check_status(self):
    self.gui.p1_t4_btn_saveTextFile.setEnabled(True)
    if self.isPeriodic == 0:
      self.gui.p1_t4_btn_DFT.setEnabled(True)
      self.gui.p1_t4_btn_IDFT.setEnabled(False)
      self.gui.p1_t4_f2.setEnabled(False)
      self.gui.p1_t4_f1.setEnabled(False)
    elif self.isPeriodic == 1:
      self.gui.p1_t4_btn_IDFT.setEnabled(True)
      self.gui.p1_t4_f2.setEnabled(True)
      self.gui.p1_t4_f1.setEnabled(True)
      self.gui.p1_t4_btn_DFT.setEnabled(False)
    else:
      self.gui.p1_t4_btn_saveTextFile.setEnabled(False)

  def DFT(self):
    self.complexList = self.dsp_class.DFT(self.secondCoulmn)

    self.firstCoulmn=[]
    self.secondCoulmn=[]
    for i in range(self.N1):
      amp = np.sqrt((self.complexList[i].real ** 2) + (self.complexList[i].imag ** 2))
      amp = np.round(amp, 11)
      phase = math.atan2(self.complexList[i].imag, self.complexList[i].real)
      phase = np.round(phase, 12)
      self.firstCoulmn.append(amp)
      self.secondCoulmn.append(phase)

    self.isPeriodic = 1
    self.fill_table()

  def IDFT(self):
    self.complexList = []
    for i in range(self.N1):
      real = self.firstCoulmn[i] * np.cos(self.secondCoulmn[i])
      imag = self.firstCoulmn[i] * np.sin(self.secondCoulmn[i])
      self.complexList.append(complex(real, imag))
      self.firstCoulmn[i] = i

    self.secondCoulmn = self.dsp_class.IDFT(self.complexList)
    self.isPeriodic = 0
    self.fill_table()

  def editOnsampleData(self):
    sampleNo = self.gui.p1_t4_f2_flineEdit_sampleNumber.text()
    newAmplitude = self.gui.p1_t4_f2_flineEdit_amplitude.text()
    newPhaseShift = self.gui.p1_t4_f2_flineEdit_phaseShift.text()
    if len(sampleNo)==0 or len(newAmplitude)==0 or len(newPhaseShift)==0:
      self.gui.p1_label_result.setText("Error: There exist empty field")
      return

    self.firstCoulmn[int(sampleNo)-1] = float(newAmplitude)
    self.secondCoulmn[int(sampleNo)-1] = float(newPhaseShift)
    self.fill_table()

  def save_in_file(self):
    # Specify the file path where you want to save the data
    fileName = str(self.gui.p1_t4_flineEdit_fileName.text())
    data={
      "signalType": self.signalType,
      "isPeriodic": self.isPeriodic,
      "N1": self.N1,
      "firstCoulmn": self.firstCoulmn,
      "secondCoulmn": self.secondCoulmn,
    }
    self.dsp_class.save_in_file(fileName, data)

  def generate_graphData(self):
    if self.isPeriodic==0:
      return

    self.sample_frequency = self.gui.p1_t4_f1_flineEdit_sampleFreq.text()
    if len(self.sample_frequency)==0:
      self.gui.p1_label_result.setText("Error: Please enter sampling frequency")
      return

    self.sample_frequency = int(self.sample_frequency)
    omegaValue = (2 * np.pi * self.sample_frequency) / self.N1

    self.omega = []
    for i in range(self.N1):
      self.omega.append(omegaValue*(i+1))

    self.generate_stemGraph()

  def generate_stemGraph(self):
    # Create a figure and two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    ax1.stem(self.omega, self.firstCoulmn)
    ax1.set_xlabel('Frequency')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Frequency vs Amplitude')

    ax2.stem(self.omega, self.secondCoulmn)
    ax2.set_xlabel('Frequency')
    ax2.set_ylabel('Phase Shift')
    ax2.set_title('Frequency vs PhaseShift')

    # Add a title to the entire figure
    fig.suptitle('Graphs')
    plt.show()

  def testResult(self):
    filePath = str(self.gui.p1_lineEdit_filePath.text())
    signalType, isPeriodic, N1, firstTestCoulmn, secondTestCoulmn = self.dsp_class.readData(filePath)
    result_text=""
    if self.isPeriodic==-1:
      result_text = "Error: Please generate table fisrt"
    elif self.isPeriodic == 0:
      result_text = SignalSamplesAreEqual(filePath, self.firstCoulmn, self.secondCoulmn)
    elif self.isPeriodic==1:
      for i in range(N1):
        firstTestCoulmn[i] = round(firstTestCoulmn[i], 11)
        secondTestCoulmn[i] = round(secondTestCoulmn[i], 12)

      ampTest = SignalComapreAmplitude(self.firstCoulmn, firstTestCoulmn)
      phaseTest = SignalComaprePhaseShift(self.secondCoulmn, secondTestCoulmn)
      if ampTest and phaseTest:
        result_text = "Test case passed successfully"
      else:
        result_text = "Test case failed, your signal have different values or length from the expected one"
    self.gui.p1_label_result.setText(result_text)
