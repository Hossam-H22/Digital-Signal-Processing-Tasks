import numpy as np
from test_scripts.task1_comparesignals import SignalSamplesAreEqual


class Task1:
  def __init__(self, dsp_class, gui):
    self.dsp_class = dsp_class
    self.gui = gui
    self.setupTask()

  def setupTask(self):
    self.gui.p1_t1_f1_btn_generationGraph.clicked.connect(self.generate_and_display_signal_task1)  # connect button to function generation graph (manual input)
    self.gui.p1_t1_f2_btn_openFile.clicked.connect(lambda: self.dsp_class.openFile(self.gui.p1_t1_f2_flineEdit_filePath))  # connect button to open file in task 1 to read signal
    self.gui.p1_t1_f2_btn_generationGraph.clicked.connect(self.generate_graph_from_file_task1)  # connect button to function generation graph (from file)
    print('Task 1 Build Successfully')

  def calcSinSignal(self, amplitude, phaseShift, analogFreq, samplingFreq):
    time = np.arange(0, 1, 1 / samplingFreq)
    signalSamples = amplitude * np.sin(2 * np.pi * analogFreq * time + phaseShift)
    return time, signalSamples

  def calcCosSignal(self, amplitude, phaseShift, analogFreq, samplingFreq):
    time = np.arange(0, 1, 1 / samplingFreq)
    signalSamples = amplitude * np.cos(2 * np.pi * analogFreq * time + phaseShift)
    return time, signalSamples

  def generate_signal(self):
    signal_type = self.gui.p1_t1_f1_comboBox_signalType.currentIndex()
    if signal_type == 1:
      signal_type = "cos"
    elif signal_type == 2:
      signal_type = "sin"

    amplitude = float(self.gui.p1_t1_f1_lineEdit_amplitude.text())
    analog_frequency = float(self.gui.p1_t1_f1_lineEdit_analogFrequency.text())
    sampling_frequency = float(self.gui.p1_t1_f1_lineEdit_samplingFrequency.text())
    phase_shift = float(self.gui.p1_t1_f1_lineEdit_phaseShift.text())

    if sampling_frequency == 0: sampling_frequency = 100

    if signal_type == 'cos':
      time, signalSamples = self.calcCosSignal(amplitude, phase_shift, analog_frequency, sampling_frequency)
    else:
      time, signalSamples = self.calcSinSignal(amplitude, phase_shift, analog_frequency, sampling_frequency)

    return time, signalSamples

  def validationInput_task1(self, type='file'):
    if self.gui.p1_t1_radioButton_manual.isChecked() and type == 'manual':
      signal_type = self.gui.p1_t1_f1_comboBox_signalType.currentIndex()
      amplitude = len(self.gui.p1_t1_f1_lineEdit_amplitude.text())
      analog_frequency = len(self.gui.p1_t1_f1_lineEdit_analogFrequency.text())
      sampling_frequency = len(self.gui.p1_t1_f1_lineEdit_samplingFrequency.text())
      phase_shift = len(self.gui.p1_t1_f1_lineEdit_phaseShift.text())

      if (signal_type <= 0 or amplitude == 0 or analog_frequency == 0 or sampling_frequency == 0 or phase_shift == 0):
        self.gui.p1_label_result.setText("Error: There is Empty Field")
        return 0
      else: return 1

    elif self.gui.p1_t1_radioButton_readFile.isChecked() and type == 'file':
      filePath = self.gui.p1_t1_f2_flineEdit_filePath.text()
      if len(filePath) == 0:
        self.gui.p1_label_result.setText("Error: Please Choose File")
        return 0
      else: return 1

    else:
      self.gui.p1_label_result.setText("Error: Please choose correct ipnut type")
      return 0

  def generate_and_display_signal_task1(self):
    if self.validationInput_task1("manual") == 0: return
    time, signalSamples = self.generate_signal()
    self.dsp_class.generate_graph(time, signalSamples)

  def generate_graph_from_file_task1(self, gui):
    if self.validationInput_task1('file') == 0: return
    file_path = gui.p1_t1_f2_flineEdit_filePath.text()
    signalType, isPeriodic, N1, time, signalSamples = self.dsp_class.readData(file_path)
    self.dsp_class.generate_graph(time, signalSamples)

  def testResult(self):
    if self.validationInput_task1('manual') == 0: return
    time, signalSamples = self.generate_signal()
    indices = np.arange(0, len(signalSamples), 1)
    result_text = SignalSamplesAreEqual(self.gui.p1_lineEdit_filePath.text(), indices, signalSamples)
    self.gui.p1_label_result.setText(result_text)
