import numpy as np
from matplotlib import pyplot as plt

from style.gui import CenteredTextLabel
from test_scripts.task1_comparesignals import SignalSamplesAreEqual
from test_scripts.task6_DerivativeSignal import DerivativeSignal
from test_scripts.task6_Shift_Fold_Signal import Shift_Fold_Signal


class Task6:
  def __init__(self, dsp_class, gui):
      self.dsp_class = dsp_class
      self.gui = gui
      self.setupTask()


  def setupTask(self):
      self.clearTable()
      self.gui.p1_t6_btn_openFile.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t6_flineEdit_filePath))  # connect button to open file to read signal
      self.gui.p1_t6_btn_generateTable.clicked.connect(self.generate_table)
      self.gui.p1_t6_btn_clearTable.clicked.connect(self.clearTable)
      self.gui.p1_t6_btn_generateGraph.clicked.connect(self.generate_stemGraph)
      print('Task 6 Build Successfully')

  def generate_table(self):
    if not self.validationInput(): return

    filePath = self.gui.p1_t6_flineEdit_filePath.text()
    signalType, isPeriodic, N1, time, signalSamples = self.dsp_class.readData(filePath)
    self.signalType = signalType
    self.isPeriodic = isPeriodic
    self.N1 = N1
    self.time = time
    self.signalSamples = signalSamples

    self.signalProcess()
    self.fill_table()

  def signalProcess(self):
      operationIndex = self.gui.p1_t6_comboBox_operation.currentIndex()
      if operationIndex==1: self.smoothing()
      elif operationIndex==2: self.sharpening_first_derivative()
      elif operationIndex==3: self.sharpening_second_derivative()
      elif operationIndex==4:
          self.newSignalSamples = self.signalSamples.copy()
          self.delay_advance()
      elif operationIndex == 5: self.folding()
      elif operationIndex == 6:
          self.folding()
          self.delay_advance()
      elif operationIndex == 7: self.removeDC_Average()
      elif operationIndex == 8: self.removeDC_DFT_IDFT()

  def validationInput(self):
    if len(self.gui.p1_t6_flineEdit_filePath.text()) == 0:
      self.gui.p1_label_result.setText("Error: Please Choose Signal File")
      return 0

    operationIndex = self.gui.p1_t6_comboBox_operation.currentIndex()

    if operationIndex == 0:
      self.gui.p1_label_result.setText("Error: Please choose operation")
      return 0
    elif operationIndex == 1 or operationIndex == 4 or operationIndex == 6:
      if len(self.gui.p1_t6_flineEdit_x.text()) == 0:
        self.gui.p1_label_result.setText("Error: Please Enter X value")
        return 0

    return 1

  def clearTable(self):
    self.gui.p1_t6_tableWidget.clear()
    self.gui.p1_t6_tableWidget.setRowCount(0)
    # self.gui.p1_t6_flineEdit_x.setText("")

  def fill_table(self):
    self.clearTable()
    self.gui.p1_t6_tableWidget.setHorizontalHeaderLabels(('Index-Before', 'Frequency-Before', 'Index-After', 'Frequency-After'))
    self.gui.p1_t6_tableWidget.setRowCount(self.N1)

    for i in range(self.N1):
      self.gui.p1_t6_tableWidget.setCellWidget(i, 0, CenteredTextLabel( str(self.time[i]) ))
      self.gui.p1_t6_tableWidget.setCellWidget(i, 1, CenteredTextLabel( str(self.signalSamples[i]) ))
      if i < len(self.newSignalSamples):
        self.gui.p1_t6_tableWidget.setCellWidget(i, 2, CenteredTextLabel( str(self.newTime[i]) ))
        self.gui.p1_t6_tableWidget.setCellWidget(i, 3, CenteredTextLabel( str(self.newSignalSamples[i]) ))
      else:
        self.gui.p1_t6_tableWidget.setCellWidget(i, 2, CenteredTextLabel(str('-')))
        self.gui.p1_t6_tableWidget.setCellWidget(i, 3, CenteredTextLabel(str('-')))

  def removeDC_Average(self):
      sum = 0
      for i in range(self.N1):
          sum += self.signalSamples[i]

      avg = sum / self.N1
      self.newSignalSamples = np.zeros(self.N1)
      for i in range(self.N1):
          self.newSignalSamples[i] = round(self.signalSamples[i] - avg, 3)

      self.newTime = self.time.copy()

  def removeDC_DFT_IDFT(self):
      try:
          # DFT
          self.complexList = []
          for i in range(self.N1):
              item = complex(0, 0)
              for j in range(self.N1):
                  power = (2 * np.pi * i * j) / self.N1
                  newItem = complex(self.signalSamples[j] * np.cos(power), self.signalSamples[j] * np.sin(power) * -1)
                  item += newItem
              self.complexList.append(item)

          self.complexList[0] = complex(0, 0)

          self.newSignalSamples = np.zeros(self.N1)
          # IDFT
          for i in range(self.N1):
              item = complex(0, 0)
              for j in range(self.N1):
                  power = (2 * np.pi * i * j) / self.N1
                  newItem = complex(np.cos(power), np.sin(power))
                  item += (newItem * self.complexList[j])
              self.newSignalSamples[i] = np.round(item.real / self.N1, 3)

          self.newTime = self.time.copy()
      except Exception as e:
          self.gui.p1_label_result.setText(e)

  def smoothing(self):
      window = int(self.gui.p1_t6_flineEdit_x.text())
      self.newSignalSamples = []
      for i in range(len(self.signalSamples) - window + 1):
          average = round(sum(self.signalSamples[i: i+window]) / window, 6)
          self.newSignalSamples.append(average)

      self.newTime = np.arange(len(self.newSignalSamples))

  def sharpening_first_derivative(self):
      self.newSignalSamples = []
      for i in range(1, self.N1):
          self.newSignalSamples.append(self.signalSamples[i] - self.signalSamples[i - 1])
      self.newTime = np.arange(len(self.newSignalSamples))

  def sharpening_second_derivative(self):
      self.newSignalSamples = []
      for i in range(1, self.N1-1):
          self.newSignalSamples.append( self.signalSamples[i+1] + self.signalSamples[i-1] - (2*self.signalSamples[i]) )
      self.newTime = np.arange(len(self.newSignalSamples))

  def folding(self):
      self.newSignalSamples = self.signalSamples[::-1]
      self.newTime = self.time.copy()

  def delay_advance(self):
      k = int(self.gui.p1_t6_flineEdit_x.text())
      self.newTime = self.time.copy()
      self.newTime = np.array(self.newTime) + k

  def generate_stemGraph(self):
    if not self.validationInput(): return
    self.generate_table()

    # Create a figure and two subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    ax1.stem(self.time, self.signalSamples)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Before')

    ax2.stem(self.newTime, self.newSignalSamples)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Frequency')
    ax2.set_title('After')

    # Add a title to the entire figure
    fig.suptitle('Graphs')
    plt.show()

  def testResult(self):
    operationIndex = self.gui.p1_t6_comboBox_operation.currentIndex()

    if not self.validationInput and operationIndex!=2 and operationIndex!=3:
        self.gui.p1_label_result.setText("Error")
        return

    if operationIndex==2 or operationIndex==3: result_text = DerivativeSignal()
    elif operationIndex==4 or operationIndex==5 or operationIndex==6:
        print("heeeree")
        result_text = Shift_Fold_Signal(self.gui.p1_lineEdit_filePath.text(), self.newTime, self.newSignalSamples)
    else: result_text = SignalSamplesAreEqual(self.gui.p1_lineEdit_filePath.text(), self.newTime, self.newSignalSamples)
    self.gui.p1_label_result.setText(result_text)