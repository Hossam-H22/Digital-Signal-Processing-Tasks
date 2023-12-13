import numpy as np
from style.gui import CenteredTextLabel
from test_scripts.task8_CompareSignal import Compare_Signals


class Task8:
  def __init__(self, dsp_class, gui):
      self.dsp_class = dsp_class
      self.gui = gui
      self.setupTask()

  def setupTask(self):
      self.clearTable()
      self.gui.p1_t8_btn_openFile.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t8_flineEdit_filePath))  # connect button to open file to read signal
      self.gui.p1_t8_btn_openFile_2.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t8_flineEdit_filePath_2))  # connect button to open file to read signal
      self.gui.p1_t8_btn_generateTable.clicked.connect(self.generate_table)
      self.gui.p1_t8_btn_clearTable.clicked.connect(self.clearTable)
      # print("Task 8 not implemented yet")
      print('Task 8 Build Successfully')

  def generate_table(self):
      if not self.validationInput(): return

      filePath1 = self.gui.p1_t8_flineEdit_filePath.text()
      self.signalType1, self.isPeriodic1, self.N1, self.time1, self.signalSamples1 = self.dsp_class.readData(filePath1)

      if self.gui.p1_t8_comboBox_correlationType.currentIndex()==2:
        filePath2 = self.gui.p1_t8_flineEdit_filePath_2.text()
        self.signalType2, self.isPeriodic2, self.N2, self.time2, self.signalSamples2 = self.dsp_class.readData(filePath2)

      if self.gui.p1_t8_comboBox_correlationType.currentIndex() == 1:
        self.autoCorrelation()
      else:
          self.crossCorrelation()
      self.fill_table()

  def autoCorrelation(self):
      self.signalSamples2=[]
      self.time2=[]

      for i in range(self.N1):
          self.signalSamples2.append(self.signalSamples1[i])
          self.time2.append(self.time1)


      if self.gui.p1_t8_comboBox_method.currentIndex() == 1:
          self.correlation_fast()
      else:
          self.correlation_direct()

      if self.gui.p1_t8_comboBox_outRange.currentIndex()==1:
          for i in range(self.N1):
              normalizeValue = self.normalization(i)
              self.correlation[i]= round(self.correlation[i]/normalizeValue, 8)

  def crossCorrelation(self):
      if self.gui.p1_t8_comboBox_method.currentIndex() == 1:
          self.correlation_fast()
      else:
          self.correlation_direct()

      if self.gui.p1_t8_comboBox_outRange.currentIndex()==1:
          for i in range(self.N1):
              normalizeValue = self.normalization(i)
              self.correlation[i]= round(self.correlation[i]/normalizeValue, 8)

  def validationInput(self):
      if self.gui.p1_t8_comboBox_correlationType.currentIndex()==0:
          self.gui.p1_label_result.setText("Error: Please Choose Correlation Type")
          return 0

      if len(self.gui.p1_t8_flineEdit_filePath.text()) == 0:
          self.gui.p1_label_result.setText("Error: Please Choose First Signal File")
          return 0

      if len(self.gui.p1_t8_flineEdit_filePath_2.text())==0 and self.gui.p1_t8_comboBox_correlationType.currentIndex()==2:
          self.gui.p1_label_result.setText("Error: Please Choose Second Signal File")
          return 0

      if self.gui.p1_t8_comboBox_outRange.currentIndex()==0:
          self.gui.p1_label_result.setText("Error: Please Choose Range Type")
          return 0

      if self.gui.p1_t8_comboBox_method.currentIndex()==0:
          self.gui.p1_label_result.setText("Error: Please Choose Method")
          return 0

      return 1

  def correlation_direct(self):
      self.correlation = []
      for i in range(self.N1):
          sum=0
          for j in range(self.N1):
              secondPart = self.signalSamples2[(j + i) % self.N1]
              if self.isPeriodic1==0 and (j+i) >= self.N1: secondPart=0
              sum += self.signalSamples1[j]*secondPart

          sum = sum/self.N1
          self.correlation.append(sum)

  def correlation_fast(self):
      # Start DFT
      self.complexList1 = []
      self.complexList2 = []
      for i in range(self.N1):
          item1 = complex(0, 0)
          item2 = complex(0, 0)
          for j in range(self.N1):
              power = (2 * np.pi * i * j) / self.N1
              # compute complex sample of signal 1
              newItem1 = complex(self.signalSamples1[j] * np.cos(power), self.signalSamples1[j] * np.sin(power) * -1)
              item1 += newItem1

              # compute complex sample of signal 2
              newItem2 = complex(self.signalSamples2[j] * np.cos(power), self.signalSamples2[j] * np.sin(power) * -1)
              item2 += newItem2

          self.complexList1.append(item1)
          self.complexList2.append(item2)
      # End DFT


      # conjugate first complex list
      for i in range(self.N1):
          self.complexList1[i] = complex(self.complexList1[i].real, self.complexList1[i].imag * -1)


      # X1*(K) . X2(K)
      self.complexListFinal = []
      for i in range(self.N1):
          self.complexListFinal.append(self.complexList1[i] * self.complexList2[i])



      # Start IDFT
      self.correlation = []
      for i in range(self.N1):
          item = complex(0, 0)
          for j in range(self.N1):
              power = (2 * np.pi * i * j) / self.N1
              newItem = complex(np.cos(power), np.sin(power))
              item += (newItem * self.complexListFinal[j])
          self.correlation.append(np.round(item.real/self.N1, 1))
      # End IDFT

      # IDFT/N
      for i in range(self.N1):
          self.correlation[i] = round(self.correlation[i]/self.N1, 2)

  def normalization(self, shift):
      sum1=0
      sum2=0

      for i in range(self.N1):
          sum1 += np.power(self.signalSamples1[i], 2)
          secondPart = self.signalSamples2[(i+shift) % self.N1]
          if self.isPeriodic1 == 0 and (i+shift)>=self.N1: secondPart = 0
          sum2 += np.power(secondPart, 2)

      normalize = round((np.sqrt(sum1*sum2))/self.N1, 1)

      return normalize

  def clearTable(self):
      self.gui.p1_t8_tableWidget.clear()
      self.gui.p1_t8_tableWidget.setRowCount(0)

  def fill_table(self):
      self.clearTable()
      self.gui.p1_t8_tableWidget.setHorizontalHeaderLabels(
          ('Index-1', 'Frequency-1', 'Index-2', 'Frequency-2', 'Correlation'))
      self.gui.p1_t8_tableWidget.setRowCount(self.N1)

      for i in range(self.N1):
          self.gui.p1_t8_tableWidget.setCellWidget(i, 0, CenteredTextLabel(str(self.time1[i])))
          self.gui.p1_t8_tableWidget.setCellWidget(i, 1, CenteredTextLabel(str(self.signalSamples1[i])))

          if self.gui.p1_t8_comboBox_correlationType.currentIndex()==2:
              self.gui.p1_t8_tableWidget.setCellWidget(i, 2, CenteredTextLabel(str(self.time2[i])))
              self.gui.p1_t8_tableWidget.setCellWidget(i, 3, CenteredTextLabel(str(self.signalSamples2[i])))
          else:
              self.gui.p1_t8_tableWidget.setCellWidget(i, 2, CenteredTextLabel(str('-')))
              self.gui.p1_t8_tableWidget.setCellWidget(i, 3, CenteredTextLabel(str('-')))

          self.gui.p1_t8_tableWidget.setCellWidget(i, 4, CenteredTextLabel(str(self.correlation[i])))

  def testResult(self):
      if not self.validationInput(): return
      self.generate_table()
      filePath = str(self.gui.p1_lineEdit_filePath.text())
      self.timeFinal = np.arange(0, self.N1)
      result_text = Compare_Signals(filePath, self.timeFinal, self.correlation)
      self.gui.p1_label_result.setText(result_text)

