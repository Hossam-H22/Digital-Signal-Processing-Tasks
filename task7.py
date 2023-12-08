import numpy as np
from matplotlib import pyplot as plt
from test_scripts.task7_ConvTest import ConvTest
from style.gui import CenteredTextLabel


class Task7:
  def __init__(self, dsp_class, gui):
      self.dsp_class = dsp_class
      self.gui = gui
      self.setupTask()


  def setupTask(self):
      self.clearTable()
      self.gui.p1_t7_btn_openFile.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t7_flineEdit_filePath))  # connect button to open file to read signal
      self.gui.p1_t7_btn_openFile_2.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t7_flineEdit_filePath_2))  # connect button to open file to read signal
      self.gui.p1_t7_btn_generateTable.clicked.connect(self.generate_table)
      self.gui.p1_t7_btn_clearTable.clicked.connect(self.clearTable)
      self.gui.p1_t7_btn_generateGraph.clicked.connect(self.generate_stemGraph)
      # print("Task 7 not implemented yet")
      print('Task 7 Build Successfully')

  def generate_table(self):
      if not self.validationInput(): return

      filePath1 = self.gui.p1_t7_flineEdit_filePath.text()
      filePath2 = self.gui.p1_t7_flineEdit_filePath_2.text()
      self.signalType1, self.isPeriodic1, self.N1, self.time1, self.signalSamples1 = self.dsp_class.readData(filePath1)
      self.signalType2, self.isPeriodic2, self.N2, self.time2, self.signalSamples2 = self.dsp_class.readData(filePath2)

      self.convolution()
      self.fill_table()

  def convolution(self):
      firstIndex = min(self.time1) + min(self.time2)
      lastIndex = max(self.time1) + max(self.time2)

      self.timeFinal = list(range(firstIndex, lastIndex + 1))
      self.N3 = lastIndex - firstIndex + 1
      self.signalSamplesFinal = np.zeros(self.N3)

      for i in range(self.N3):
          for iX in range(self.N1):
              iH = i - iX
              if iH >= 0 and iH < self.N2:
                  self.signalSamplesFinal[i] += self.signalSamples1[iX] * self.signalSamples2[iH]

  def validationInput(self):
      if len(self.gui.p1_t7_flineEdit_filePath.text()) == 0 or len(self.gui.p1_t7_flineEdit_filePath_2.text()) == 0:
          self.gui.p1_label_result.setText("Error: Please Choose Signal Files")
          return 0

      return 1

  def clearTable(self):
      self.gui.p1_t7_tableWidget.clear()
      self.gui.p1_t7_tableWidget.setRowCount(0)

  def fill_table(self):
      self.clearTable()
      self.gui.p1_t7_tableWidget.setHorizontalHeaderLabels(
          ('Index-1', 'Frequency-1', 'Index-2', 'Frequency-2', 'Index-Final', 'Frequency-Final'))
      self.gui.p1_t7_tableWidget.setRowCount(self.N3)

      for i in range(self.N3):
          if i < self.N1:
              self.gui.p1_t7_tableWidget.setCellWidget(i, 0, CenteredTextLabel(str(self.time1[i])))
              self.gui.p1_t7_tableWidget.setCellWidget(i, 1, CenteredTextLabel(str(self.signalSamples1[i])))
          else:
              self.gui.p1_t7_tableWidget.setCellWidget(i, 0, CenteredTextLabel(str('-')))
              self.gui.p1_t7_tableWidget.setCellWidget(i, 1, CenteredTextLabel(str('-')))


          if i < self.N2:
              self.gui.p1_t7_tableWidget.setCellWidget(i, 2, CenteredTextLabel(str(self.time2[i])))
              self.gui.p1_t7_tableWidget.setCellWidget(i, 3, CenteredTextLabel(str(self.signalSamples2[i])))
          else:
              self.gui.p1_t7_tableWidget.setCellWidget(i, 2, CenteredTextLabel(str('-')))
              self.gui.p1_t7_tableWidget.setCellWidget(i, 3, CenteredTextLabel(str('-')))


          self.gui.p1_t7_tableWidget.setCellWidget(i, 4, CenteredTextLabel(str(self.timeFinal[i])))
          self.gui.p1_t7_tableWidget.setCellWidget(i, 5, CenteredTextLabel(str(self.signalSamplesFinal[i])))

  def generate_stemGraph(self):
      if not self.validationInput(): return
      self.generate_table()

      # Create a figure and two subplots
      fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 5))

      ax1.stem(self.time1, self.signalSamples1)
      ax1.set_xlabel('Time')
      ax1.set_ylabel('Frequency')
      ax1.set_title('1th')

      ax2.stem(self.time2, self.signalSamples2)
      ax2.set_xlabel('Time')
      ax2.set_ylabel('Frequency')
      ax2.set_title('2th')

      ax3.stem(self.timeFinal, self.signalSamplesFinal)
      ax3.set_xlabel('Time')
      ax3.set_ylabel('Frequency')
      ax3.set_title('Final')


      # Add a title to the entire figure
      fig.suptitle('Graphs')
      plt.show()

  def testResult(self):
      if not self.validationInput(): return
      self.generate_table()
      result_text = ConvTest(self.timeFinal, self.signalSamplesFinal)
      self.gui.p1_label_result.setText(result_text)

