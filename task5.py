import numpy as np
from style.gui import CenteredTextLabel
from test_scripts.task5_comparesignal2 import *


class Task5:
  def __init__(self, dsp_class, gui):
      self.dsp_class = dsp_class
      self.gui = gui
      self.setupTask()

  def setupTask(self):
      self.clearTable()
      self.isPeriodic = -1
      self.gui.p1_t5_btn_openFile.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t5_flineEdit_filePath))  # connect button to open file to read signal
      self.gui.p1_t5_btn_generateTable.clicked.connect(lambda: self.generate_table_from_file(self.gui.p1_t5_flineEdit_filePath.text()))
      self.gui.p1_t5_btn_clearTable.clicked.connect(self.clearTable)
      self.gui.p1_t5_btn_DCT.clicked.connect(self.DCT)
      self.gui.p1_t5_btn_RemoveDC.clicked.connect(self.removeDC)
      self.gui.p1_t5_f1_btn_saveTextFile.clicked.connect(self.save_in_file)
      # print("Task 5 not implemented yet")
      print('Task 5 Build Successfully')

  def clearTable(self):
    self.gui.p1_t5_tableWidget.clear()
    self.gui.p1_t5_tableWidget.setRowCount(0)
    self.gui.p1_t5_f1.setEnabled(False)
    self.gui.p1_t5_btn_DCT.setEnabled(False)
    self.gui.p1_t5_btn_RemoveDC.setEnabled(False)
    self.gui.p1_t5_f1_flineEdit_fileName.setText("")
    self.gui.p1_t5_f1_flineEdit_numberSamples.setText("")

  def generate_table_from_file(self, filePath):
    if len(filePath) == 0:
      self.gui.p1_label_result.setText("Error: Please Choose Signal File")
      return

    signalType, isPeriodic, N1, time, signalSamples = self.dsp_class.readData(filePath)
    self.signalType = signalType
    self.isPeriodic = isPeriodic
    self.N1 = N1
    self.time = time
    self.signalSamples = signalSamples
    self.fill_table()

  def fill_table(self):
    self.clearTable()
    self.gui.p1_t5_f1.setEnabled(True)
    self.gui.p1_t5_btn_DCT.setEnabled(True)
    self.gui.p1_t5_btn_RemoveDC.setEnabled(True)

    if self.isPeriodic==0:
      self.gui.p1_t5_tableWidget.setHorizontalHeaderLabels(('Index', 'Frequency'))
    elif self.isPeriodic==1:
      self.gui.p1_t5_tableWidget.setHorizontalHeaderLabels(('Amplitude', 'Phase Shift'))

    self.gui.p1_t5_tableWidget.setRowCount(self.N1)
    for i in range(self.N1):
      self.gui.p1_t5_tableWidget.setCellWidget(i, 0, CenteredTextLabel( str(self.time[i]) ))
      self.gui.p1_t5_tableWidget.setCellWidget(i, 1, CenteredTextLabel( str(self.signalSamples[i]) ))

  def removeDC(self):
      sum = 0
      for i in range(self.N1):
          sum += self.signalSamples[i]

      avg = sum / self.N1
      for i in range(self.N1):
          self.signalSamples[i] = round(self.signalSamples[i] - avg, 3)

      self.fill_table()

  def DCT(self):
      self.dct = np.zeros(self.N1)

      for k in range(self.N1):
          sum = 0
          for n1 in range(self.N1):
              sum += (self.signalSamples[n1] * np.cos((np.pi / (4 * self.N1)) * ((2 * n1) - 1) * ((2 * k) - 1)))
          self.dct[k] = sum * np.sqrt(2 / self.N1)

      self.signalSamples = self.dct
      self.fill_table()

  def save_in_file(self):
    noSamples = self.gui.p1_t5_f1_flineEdit_numberSamples.text()
    if len(noSamples)==0: N = self.N1
    else: N = int(noSamples)

    # Specify the file path where you want to save the data
    fileName = str(self.gui.p1_t5_f1_flineEdit_fileName.text())
    data = {
        "signalType": self.signalType,
        "isPeriodic": self.isPeriodic,
        "N1": N,
        "firstCoulmn": self.time,
        "secondCoulmn": self.signalSamples[:N],
    }
    self.dsp_class.save_in_file(fileName, data)

  def testResult(self):
    filePath = str(self.gui.p1_lineEdit_filePath.text())
    if self.isPeriodic==-1: result_text = "Error: Please generate table fisrt"
    else: result_text = SignalSamplesAreEqual(filePath, self.signalSamples)
    self.gui.p1_label_result.setText(result_text)
