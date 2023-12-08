
import numpy as np
from test_scripts.task1_comparesignals  import SignalSamplesAreEqual
from test_scripts.task2_TEST import *

class Task2:
  def __init__(self, dsp_class, gui):
    self.dsp_class = dsp_class
    self.gui = gui
    self.setupTask()

  def setupTask(self):
    self.gui.p1_t2_btn_openFile.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t2_flineEdit_filePath))  # connect button to open file in task 2 to read signal 1
    self.gui.p1_t2_btn_openFile_2.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t2_flineEdit_filePath_2))  # connect button to open file in task 2 to read signal 2
    self.gui.p1_t2_btn_generateGraph_result.clicked.connect(self.generate_and_display_signal_task2)  # connect button to function generation graph after operation on signal
    self.gui.p1_t2_btn_generateGraph.clicked.connect(lambda: self.generate_graph_from_file_task2(self.gui.p1_t2_flineEdit_filePath.text()))
    self.gui.p1_t2_btn_generateGraph_2.clicked.connect(lambda: self.generate_graph_from_file_task2(self.gui.p1_t2_flineEdit_filePath_2.text()))
    print('Task 2 Build Successfully')

  def simpleOperationOnTwoSignals(self, operationIndex):
    signalType1, isPeriodic1, N11, time1, signalSamples1 = self.dsp_class.readData(self.gui.p1_t2_flineEdit_filePath.text())
    signalType2, isPeriodic2, N12, time2, signalSamples2 = self.dsp_class.readData(self.gui.p1_t2_flineEdit_filePath_2.text())

    signalSamples = []
    if operationIndex == 1:  # Addition
      signalSamples = [a + b for a, b in zip(signalSamples1, signalSamples2)]
    elif operationIndex == 2:  # Subtraction
      signalSamples = [b - a for a, b in zip(signalSamples1, signalSamples2)]
    else:  # Multiplication
      signalSamples = [a * b for a, b in zip(signalSamples1, signalSamples2)]

    return time1, signalSamples

  def simpleOperationOnOneSignal(self, operationIndex):
    signalType1, isPeriodic1, N11, time1, signalSamples1 = self.dsp_class.readData(self.gui.p1_t2_flineEdit_filePath.text())
    x = int(self.gui.p1_t2_flineEdit_x.text())
    self.x = x

    signalSamples = signalSamples1

    if operationIndex == 4:  # Multiply
      signalSamples = [i * x for i in signalSamples1]
    elif operationIndex == 5:  # Power
      signalSamples = np.power(signalSamples1, x)
    else:  # Shifting
      time1 = [i + x for i in time1]

    return time1, signalSamples

  def normalization(self):
    signalType1, isPeriodic1, N11, time1, signalSamples1 = self.dsp_class.readData(self.gui.p1_t2_flineEdit_filePath.text())
    x = int(self.gui.p1_t2_flineEdit_x.text())
    y = int(self.gui.p1_t2_flineEdit_y.text())

    if x > y:
      x, y = y, x

    self.x = x
    self.y = y

    minimum_value = min(signalSamples1)
    maximum_value = max(signalSamples1)

    signalSamples = []
    for i in signalSamples1:
      value = (((i - minimum_value) / (maximum_value - minimum_value)) * (y - x)) + x
      signalSamples.append(value)

    return time1, signalSamples

  def accumulation(self):
    signalType1, isPeriodic1, N11, time1, signalSamples1 = self.dsp_class.readData(self.gui.p1_t2_flineEdit_filePath.text())

    signalSamples = []
    sum = 0
    for i in signalSamples1:
      sum += i
      signalSamples.append(sum)

    return time1, signalSamples

  def validationInput_task2(self):
    if len(self.gui.p1_t2_flineEdit_filePath.text()) == 0:
      self.gui.p1_label_result.setText("Error: Please Choose First Signal File")
      return 0

    operationIndex = self.gui.p1_t2_comboBox_operation.currentIndex()

    if operationIndex == 0:
      self.gui.p1_label_result.setText("Error: Please choose operation")
      return 0
    elif operationIndex == 1 or operationIndex == 2 or operationIndex == 3:
      if len(self.gui.p1_t2_flineEdit_filePath_2.text()) == 0:
        self.gui.p1_label_result.setText("Error: Please Choose Second Signal File")
        return 0
    elif operationIndex == 4 or operationIndex == 5 or operationIndex == 6:
      if len(self.gui.p1_t2_flineEdit_x.text()) == 0:
        self.gui.p1_label_result.setText("Error: Please Enter X value")
        return 0
    elif operationIndex == 7:
      if len(self.gui.p1_t2_flineEdit_x.text()) == 0:
        self.gui.p1_label_result.setText("Error: Please Enter X value")
        return 0
      elif len(self.gui.p1_t2_flineEdit_y.text()) == 0:
        self.gui.p1_label_result.setText("Error: Please Enter Y value")
        return 0

    return 1

  def generate_resultSignal(self):
    operationIndex = self.gui.p1_t2_comboBox_operation.currentIndex()
    if operationIndex == 1 or operationIndex == 2 or operationIndex == 3:
      time, signalSamples = self.simpleOperationOnTwoSignals(operationIndex)
    elif operationIndex == 4 or operationIndex == 5 or operationIndex == 6:
      time, signalSamples = self.simpleOperationOnOneSignal(operationIndex)
    elif operationIndex == 7:
      time, signalSamples = self.normalization()
    else:
      time, signalSamples = self.accumulation()

    return time, signalSamples

  def generate_and_display_signal_task2(self):
    if self.validationInput_task2() == 0: return
    time, signalSamples = self.generate_resultSignal()
    self.dsp_class.generate_graph(time, signalSamples)

  def generate_graph_from_file_task2(self, filePath):
    if len(filePath) == 0:
      self.gui.p1_label_result.setText("Error: Please Choose Signal File")
      return

    signalType, isPeriodic, N1, time, signalSamples = self.dsp_class.readData(filePath)
    self.dsp_class.generate_graph(time, signalSamples)

  def testResult(self):
    if self.validationInput_task2() == 0: return
    time, signalSamples = self.generate_resultSignal()
    operationIndex = self.gui.p1_t2_comboBox_operation.currentIndex()
    if operationIndex==1: result_text = AddSignalSamplesAreEqual(self.gui.p1_lineEdit_filePath.text(), time, signalSamples)
    elif operationIndex==2: result_text = SubSignalSamplesAreEqual(self.gui.p1_lineEdit_filePath.text(), time, signalSamples)
    elif operationIndex==4: result_text = MultiplySignalByConst(self.gui.p1_lineEdit_filePath.text(), self.x, time, signalSamples)
    elif operationIndex==5: result_text = SignalSamplesAreEqual('SQU', self.gui.p1_lineEdit_filePath.text(), time, signalSamples)
    elif operationIndex==6: result_text = ShiftSignalByConst(self.gui.p1_lineEdit_filePath.text(), self.x, time, signalSamples)
    elif operationIndex==7: result_text = NormalizeSignal(self.gui.p1_lineEdit_filePath.text(), self.x, self.y, time, signalSamples)
    elif operationIndex==8: result_text = SignalSamplesAreEqual('ACC', self.gui.p1_lineEdit_filePath.text(), time, signalSamples)
    else: result_text = SignalSamplesAreEqual(self.gui.p1_lineEdit_filePath.text(), time, signalSamples)
    self.gui.p1_label_result.setText(result_text)
