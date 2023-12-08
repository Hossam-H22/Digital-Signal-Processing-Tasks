import numpy as np
from PyQt5.QtWidgets import QTableWidgetItem
from style.gui import CenteredTextLabel
from test_scripts.task3_QuanTest1 import QuantizationTest1
from test_scripts.task3_QuanTest2 import QuantizationTest2

class Task3:
  def __init__(self, dsp_class, gui):
    self.dsp_class = dsp_class
    self.gui = gui
    self.setupTask()

  def setupTask(self):
    self.gui.p1_t3_btn_openFile.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t3_flineEdit_filePath))  # connect button to open file to read signal
    self.gui.p1_t3_btn_generateGraph.clicked.connect(lambda: self.generate_graph_from_file(self.gui.p1_t3_flineEdit_filePath.text()))
    self.gui.p1_t3_btn_generateGraph_2.clicked.connect(self.generate_graphAndTable)
    self.gui.p1_t3_btn_generateTable.clicked.connect(lambda: self.generate_table())
    self.gui.p1_t3_btn_clearTable.clicked.connect(self.clearTable)
    self.clearTable()
    print('Task 3 Build Successfully')

  def clearTable(self):
    self.gui.p1_t3_tableWidget.clear()
    self.gui.p1_t3_tableWidget.setHorizontalHeaderLabels(('n', 'X(n)', 'Interval Index', 'Encoded Value', 'Xq(n)', 'eq(n) = Xq(n) - X(n)', 'eq(n)^2'))
    self.gui.p1_t3_tableWidget.setColumnWidth(0, 80) # n
    self.gui.p1_t3_tableWidget.setColumnWidth(1, 100) # X(n)
    self.gui.p1_t3_tableWidget.setColumnWidth(2, 130) # Interval Index
    self.gui.p1_t3_tableWidget.setColumnWidth(3, 130) # Encoded Value
    self.gui.p1_t3_tableWidget.setColumnWidth(4, 100) # Xq(n)
    self.gui.p1_t3_tableWidget.setColumnWidth(5, 170) # eq(n) = Xq(n) - X(n)
    self.gui.p1_t3_tableWidget.setColumnWidth(6, 110) # eq(n)^2
    self.gui.p1_t3_tableWidget.setRowCount(0)
    self.gui.p1_t3_tableWidget.verticalHeader().setVisible(False)

  def generate_graph_from_file(self, filePath):
    if len(filePath) == 0:
      self.gui.p1_label_result.setText("Error: Please Choose Signal File")
      return

    signalType, isPeriodic, N1, time, signalSamples = self.dsp_class.readData(filePath)
    self.dsp_class.generate_graph(time, signalSamples)

  def input_validation(self):
    filePath = self.gui.p1_t3_flineEdit_filePath.text()
    choiceType = self.gui.p1_t3_comboBox_inputType.currentIndex()
    levels = self.gui.p1_t3_flineEdit_levels.text()
    if len(filePath) == 0:
      self.gui.p1_label_result.setText("Error: Please Choose Signal File")
      return 0
    elif choiceType == 0:
      self.gui.p1_label_result.setText("Error: Please Choose Type of Input")
      return 0
    elif len(levels) == 0:
      self.gui.p1_label_result.setText("Error: please enter levels number or size")
      return 0

    return 1

  def getLevelNumber(self):
    choiceType = self.gui.p1_t3_comboBox_inputType.currentIndex()
    levels = self.gui.p1_t3_flineEdit_levels.text()
    if choiceType==1:
      self.levelcount = int(levels)
      self.numOfbits = int(np.log2(self.levelcount))
    else:
      self.numOfbits = int(levels)
      self.levelcount = int(np.power(2, self.numOfbits))

    # print("level count: ", self.levelcount)
    # print("number of bits: ", self.numOfbits)

  def generateEncodedValues(self):
    self.encoddedvalues = []
    for i in range(self.levelcount):
      encodeValue = np.binary_repr(i)
      numOfZeros = self.numOfbits - len(encodeValue)
      for x in range(numOfZeros):
        encodeValue = '0'+encodeValue

      self.encoddedvalues.append(encodeValue)
    # print(self.encoddedvalues)

  def generateIntervalsAndMidpoints(self):
    self.intervals = []
    self.midpoints = []
    self.stepSize = (max(self.signalSamples) - min(self.signalSamples))/self.levelcount
    self.stepSize = float(f'{self.stepSize:.2f}')
    # print("step size = ", self.stepSize)
    start = min(self.signalSamples)
    end = start + self.stepSize
    for i in range(self.levelcount):
      start = float(f'{start:.2f}')
      end = float(f'{end:.2f}')
      self.intervals.append({
        'start': start,
        'end': end
      })
      midPoint = (start+end)/2
      self.midpoints.append(float(f'{midPoint:.3f}'))
      start = end
      end += self.stepSize

    # print(self.intervals)

  def generateQuantization(self):
    self.quantaizeSignalSamples = []
    self.intervalIndexs = []
    self.encodedSignalLevel = []
    for sample in self.signalSamples:
      for i in range(self.levelcount):
        if sample >= self.intervals[i]['start'] and sample <= self.intervals[i]['end']:
          self.quantaizeSignalSamples.append(self.midpoints[i])
          self.intervalIndexs.append(i+1)
          self.encodedSignalLevel.append(self.encoddedvalues[i])
          break
    # print(self.quantaizeSignalSamples)
    # print(self.intervalIndexs)
    # print("len Sample = ", len(self.signalSamples))
    # print("len Quantaization = ", len(self.quantaizeSignalSamples))

  def calculateQuantizationError(self):
    self.quantaizationError = []
    self.quantaizationErrorSquare = []
    self.averagePowerError = 0
    if len(self.quantaizeSignalSamples) != len(self.signalSamples):
      self.gui.p1_label_result.setText("Error: there is signal doesn't exist in any interval while quantization")
      return 0

    for i in range(self.N1):
      error = self.quantaizeSignalSamples[i] - self.signalSamples[i]
      error = float(f'{error:.3f}')
      self.quantaizationError.append(error)
      errorSquare = float(f'{np.power(error, 2):.4f}')
      self.quantaizationErrorSquare.append(errorSquare)
      self.averagePowerError += errorSquare

    self.averagePowerError = self.averagePowerError/self.N1
    self.averagePowerError = float(f'{self.averagePowerError:.3f}')

    return 1

  def addDataToTable(self):
    self.gui.p1_t3_tableWidget.setRowCount(self.N1+1)
    for i in range(self.N1):
      self.gui.p1_t3_tableWidget.setCellWidget(i, 0, CenteredTextLabel( str(i+1) ))
      self.gui.p1_t3_tableWidget.setCellWidget(i, 1, CenteredTextLabel( str(self.signalSamples[i]) ))
      self.gui.p1_t3_tableWidget.setCellWidget(i, 2, CenteredTextLabel( str(self.intervalIndexs[i]) ))
      self.gui.p1_t3_tableWidget.setCellWidget(i, 3, CenteredTextLabel( str(self.encodedSignalLevel[i]) ))
      self.gui.p1_t3_tableWidget.setCellWidget(i, 4, CenteredTextLabel( str(self.quantaizeSignalSamples[i]) ))
      self.gui.p1_t3_tableWidget.setCellWidget(i, 5, CenteredTextLabel( str(self.quantaizationError[i]) ))
      self.gui.p1_t3_tableWidget.setCellWidget(i, 6, CenteredTextLabel( str( self.quantaizationErrorSquare[i] ) ))

    self.gui.p1_t3_tableWidget.setSpan(self.N1, 0, self.N1, 7)
    self.gui.p1_t3_tableWidget.setCellWidget(self.N1, 0, CenteredTextLabel(str("Average Power Error = ")+str(self.averagePowerError) ))

  def generate_table(self):
    if not self.input_validation(): return 0
    self.clearTable()
    signalType, isPeriodic, N1, time, signalSamples = self.dsp_class.readData(self.gui.p1_t3_flineEdit_filePath.text())
    self.time = time
    self.signalSamples = signalSamples
    self.N1 = N1
    self.getLevelNumber()
    self.generateEncodedValues()
    self.generateIntervalsAndMidpoints()
    self.generateQuantization()
    if self.calculateQuantizationError() == 0: return 0
    self.addDataToTable()
    return 1

  def generate_graphAndTable(self):
    if self.generate_table() == 0: return
    self.dsp_class.generate_graph(self.time, self.quantaizeSignalSamples)

  def testResult(self):
    self.generate_table()
    filePath = str(self.gui.p1_lineEdit_filePath.text())
    if filePath.endswith('Quan1_Out.txt'):
      result_text = QuantizationTest1(filePath, self.encodedSignalLevel, self.quantaizeSignalSamples)
    elif filePath.endswith('Quan2_Out.txt'):
      result_text = QuantizationTest2(filePath, self.intervalIndexs, self.encodedSignalLevel, self.quantaizeSignalSamples, self.quantaizationError)
    self.gui.p1_label_result.setText(result_text)
