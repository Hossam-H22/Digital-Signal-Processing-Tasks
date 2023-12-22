import numpy as np
from matplotlib import pyplot as plt

from test_scripts.task7_ConvTest import ConvTest
from style.gui import CenteredTextLabel
from test_scripts.task8_CompareSignal import Compare_Signals


class Task9:
  def __init__(self, dsp_class, gui):
      self.dsp_class = dsp_class
      self.gui = gui
      self.setupTask()

  def setupTask(self):
      self.clearTable()
      self.gui.p1_t9_btn_openFile.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t9_flineEdit_filePath))  # connect button to open file to read signal
      self.gui.p1_t9_btn_openFile_2.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t9_flineEdit_filePath_2))  # connect button to open file to read signal
      self.gui.p1_t9_btn_generateTable.clicked.connect(self.generate_table)
      self.gui.p1_t9_btn_clearTable.clicked.connect(self.clearTable)
      # print("Task 9 not implemented yet")
      print('Task 9 Build Successfully')

  def generate_table(self):
      if not self.validationInput(): return

      filePath1 = self.gui.p1_t9_flineEdit_filePath.text()
      self.signalType1, self.isPeriodic1, self.N1, self.time1, self.signalSamples1 = self.dsp_class.readData(filePath1)

      if self.gui.p1_t9_comboBox_operationType.currentIndex()==2 or self.gui.p1_t9_comboBox_operationType.currentIndex()==3:
        filePath2 = self.gui.p1_t9_flineEdit_filePath_2.text()
        self.signalType2, self.isPeriodic2, self.N2, self.time2, self.signalSamples2 = self.dsp_class.readData(filePath2)

      if self.gui.p1_t9_comboBox_operationType.currentIndex() == 1:
        self.autoCorrelation()
      elif self.gui.p1_t9_comboBox_operationType.currentIndex() == 2:
          self.crossCorrelation()
      elif self.gui.p1_t9_comboBox_operationType.currentIndex() == 3:
          self.convolution()

      self.fill_table()

  def validationInput(self):
      if self.gui.p1_t9_comboBox_operationType.currentIndex()==0:
          self.gui.p1_label_result.setText("Error: Please Choose Operation Type")
          return 0

      if len(self.gui.p1_t9_flineEdit_filePath.text()) == 0:
          self.gui.p1_label_result.setText("Error: Please Choose First Signal File")
          return 0

      if len(self.gui.p1_t9_flineEdit_filePath_2.text())==0 and self.gui.p1_t9_comboBox_operationType.currentIndex()>=2:
          self.gui.p1_label_result.setText("Error: Please Choose Second Signal File")
          return 0

      if self.gui.p1_t9_comboBox_outRange.currentIndex()==0 and self.gui.p1_t9_comboBox_operationType.currentIndex()!=3:
          self.gui.p1_label_result.setText("Error: Please Choose Range Type")
          return 0

      if self.gui.p1_t9_comboBox_method.currentIndex()==0:
          self.gui.p1_label_result.setText("Error: Please Choose Method")
          return 0

      return 1

  def autoCorrelation(self):
      self.signalSamples2=[]
      self.time2=[]
      self.N2=0

      for i in range(self.N1):
          self.signalSamples2.append(self.signalSamples1[i])
          self.time2.append(self.time1)

      if self.gui.p1_t9_comboBox_method.currentIndex() == 1:
          self.correlation_direct()
      elif self.gui.p1_t9_comboBox_method.currentIndex() >= 2: # Fourier or Fast Fourier Method
          self.correlation_fourier()

      if self.gui.p1_t9_comboBox_outRange.currentIndex() == 1:
          for i in range(self.N1):
              normalizeValue = self.normalization(i)
              self.resultsValues[i]= round(self.resultsValues[i]/normalizeValue, 8)

      self.N3 = len(self.resultsValues)
      self.resultsIndex = list(range(0, self.N3))

  def crossCorrelation(self):
      if self.gui.p1_t9_comboBox_method.currentIndex() == 1:
          self.correlation_direct()
      elif self.gui.p1_t9_comboBox_method.currentIndex() >= 2: # Fourier or Fast Fourier Method
          self.correlation_fourier()

      if self.gui.p1_t9_comboBox_outRange.currentIndex() == 1:
          for i in range(self.N1):
              normalizeValue = self.normalization(i)
              self.resultsValues[i] = round(self.resultsValues[i]/normalizeValue, 8)

      self.N3 = len(self.resultsValues)
      self.resultsIndex = list(range(0, self.N3))

  def convolution(self):
      if self.gui.p1_t9_comboBox_method.currentIndex() == 1:
          self.convolution_direct()
      elif self.gui.p1_t9_comboBox_method.currentIndex() >= 2: # Fourier or Fast Fourier Method
          self.convolution_fourier()

  def convolution_direct(self):
      firstIndex = min(self.time1) + min(self.time2)
      lastIndex = max(self.time1) + max(self.time2)

      self.resultsIndex = list(range(firstIndex, lastIndex + 1))
      self.N3 = lastIndex - firstIndex + 1
      self.resultsValues = np.zeros(self.N3)

      for i in range(self.N3):
          for iX in range(self.N1):
              iH = i - iX
              if iH >= 0 and iH < self.N2:
                  self.resultsValues[i] += self.signalSamples1[iX] * self.signalSamples2[iH]

  def convolution_fourier(self):
      # Calculate Indexing
      firstIndex = min(self.time1) + min(self.time2)
      lastIndex = max(self.time1) + max(self.time2)
      self.resultsIndex = list(range(firstIndex, lastIndex + 1))
      self.N3 = lastIndex - firstIndex + 1

      # Expan signals with zeros
      self.signalSamples1 = self.signalSamples1 + [0]*(self.N3-self.N1)
      self.signalSamples2 = self.signalSamples2 + [0]*(self.N3-self.N2)

      # apply DFT on signals
      dftSignal1 = self.dsp_class.DFT(self.signalSamples1)
      dftSignal2 = self.dsp_class.DFT(self.signalSamples2)

      # multiply the 2 signals
      dftFinal=[]
      for i in range(self.N3): dftFinal.append(dftSignal1[i] * dftSignal2[i])

      # apply IDFT on result
      self.resultsValues = self.dsp_class.IDFT(dftFinal)

  def correlation_direct(self):
      self.resultsValues = []
      for i in range(self.N1):
          sum=0
          for j in range(self.N1):
              secondPart = self.signalSamples2[(j + i) % self.N1]
              if self.isPeriodic1==0 and (j+i) >= self.N1: secondPart=0
              sum += self.signalSamples1[j]*secondPart

          sum = sum/self.N1
          self.resultsValues.append(sum)

  def correlation_fourier(self):
      # DFT
      self.complexList1 = self.dsp_class.DFT(self.signalSamples1)
      self.complexList2 = self.dsp_class.DFT(self.signalSamples2)

      # conjugate first complex list
      for i in range(self.N1):
          self.complexList1[i] = complex(self.complexList1[i].real, self.complexList1[i].imag * -1)

      # X1*(K) . X2(K)
      self.complexListFinal = []
      for i in range(self.N1):
          self.complexListFinal.append(self.complexList1[i] * self.complexList2[i])

      # IDFT
      self.resultsValues = self.dsp_class.IDFT(self.complexListFinal)

      # IDFT/N
      for i in range(self.N1):
          self.resultsValues[i] = round(self.resultsValues[i]/self.N1, 2)

  def normalization(self, shift):
      sum1=0
      sum2=0
      for i in range(self.N1):
          sum1 += np.power(self.signalSamples1[i], 2)
          secondPart = self.signalSamples2[(i+shift) % self.N1]
          if self.isPeriodic1 == 0 and (i+shift)>=self.N1: secondPart = 0
          sum2 += np.power(secondPart, 2)

      normalizeValue = round((np.sqrt(sum1*sum2))/self.N1, 1)
      return normalizeValue

  def clearTable(self):
      self.gui.p1_t9_tableWidget.clear()
      self.gui.p1_t9_tableWidget.setRowCount(0)

  def fill_table(self):
      self.clearTable()
      self.gui.p1_t9_tableWidget.setHorizontalHeaderLabels(
          ('Index-1', 'Frequency-1', 'Index-2', 'Frequency-2', 'Index-Results', 'Values-Results'))

      N = max(self.N1, self.N2, self.N3)
      self.gui.p1_t9_tableWidget.setRowCount(N)

      for i in range(N):
          if i<self.N1:
              self.gui.p1_t9_tableWidget.setCellWidget(i, 0, CenteredTextLabel(str(self.time1[i])))
              self.gui.p1_t9_tableWidget.setCellWidget(i, 1, CenteredTextLabel(str(self.signalSamples1[i])))
          else:
              self.gui.p1_t9_tableWidget.setCellWidget(i, 0, CenteredTextLabel(str('-')))
              self.gui.p1_t9_tableWidget.setCellWidget(i, 1, CenteredTextLabel(str('-')))

          if self.gui.p1_t9_comboBox_operationType.currentIndex()>=2 and i<self.N2:
              self.gui.p1_t9_tableWidget.setCellWidget(i, 2, CenteredTextLabel(str(self.time2[i])))
              self.gui.p1_t9_tableWidget.setCellWidget(i, 3, CenteredTextLabel(str(self.signalSamples2[i])))
          else:
              self.gui.p1_t9_tableWidget.setCellWidget(i, 2, CenteredTextLabel(str('-')))
              self.gui.p1_t9_tableWidget.setCellWidget(i, 3, CenteredTextLabel(str('-')))

          if i<self.N3:
              self.gui.p1_t9_tableWidget.setCellWidget(i, 4, CenteredTextLabel(str(self.resultsIndex[i])))
              self.gui.p1_t9_tableWidget.setCellWidget(i, 5, CenteredTextLabel(str(self.resultsValues[i])))
          else:
              self.gui.p1_t9_tableWidget.setCellWidget(i, 4, CenteredTextLabel(str('-')))
              self.gui.p1_t9_tableWidget.setCellWidget(i, 5, CenteredTextLabel(str('-')))

  def testResult(self):
      if not self.validationInput(): return
      self.generate_table()
      filePath = str(self.gui.p1_lineEdit_filePath.text())
      if self.gui.p1_t9_comboBox_operationType.currentIndex() == 3:
          result_text = ConvTest(self.resultsIndex, self.resultsValues)
      else:
          result_text = Compare_Signals(filePath, self.resultsIndex, self.resultsValues)

      self.gui.p1_label_result.setText(result_text)

