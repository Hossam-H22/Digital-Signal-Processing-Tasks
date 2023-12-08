from PyQt5 import QtWidgets
from tkinter import filedialog
import matplotlib.pyplot as plt
import sys
import os

from style.design import Ui_MainWindow
from style.gui import GUI
from task1 import Task1
from task2 import Task2
from task3 import Task3
from task4 import Task4
from task5 import Task5
from task6 import Task6
from task7 import Task7
from task8 import Task8


class DspGenerale:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        # self.gui = GUI()
        self.gui = Ui_MainWindow()
        self.task1 = Task1(self, self.gui)
        self.task2 = Task2(self, self.gui)
        self.task3 = Task3(self, self.gui)
        self.task4 = Task4(self, self.gui)
        self.task5 = Task5(self, self.gui)
        self.task6 = Task6(self, self.gui)
        self.task7 = Task7(self, self.gui)
        # self.task8 = Task8(self, self.gui)

        self.setupTask()
        self.gui.show()

        sys.exit(self.app.exec_())

    def setupTask(self):
        self.gui.p1_btn_openTestFile.clicked.connect(lambda: self.openFile(self.gui.p1_lineEdit_filePath))  # connect result button to open file
        self.gui.p1_btn_clearResult.clicked.connect(self.clearResultLabel)  # connect to clear result function
        self.gui.p1_btn_test.clicked.connect(self.testResults)  # connect to test results function

    def readData(self, file_name):

        with open(file_name, "r") as file:
            signalType = int(file.readline())
            isPeriodic = int(file.readline())
            N1 = int(file.readline())
            input = file.read()

        # Split the data into lines
        lines = input.split('\n')

        time = []
        signalSamples = []
        amp=[]
        phaseShift = []

        # Process each line
        for line in lines:
            
            valuesTry1 = line.split(' ')
            valuesTry2 = line.split(',')
            if len(valuesTry2)==2: values = valuesTry2
            else: values = valuesTry1

            if isPeriodic==0:
                time.append(int(values[0]))
                signalSamples.append(float(values[1]))
            elif isPeriodic==1:
                amp.append(float( values[0].replace('f', '') ))
                phaseShift.append(float( values[1].replace('f', '') ))

        return (signalType,
                isPeriodic,
                N1,
                time if len(time)!=0 else amp,
                signalSamples if len(signalSamples)!=0 else phaseShift)

    def generate_graph(self, time, signalSamples):
        # Create a figure and two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

        # Continuous Signal Representation
        ax1.plot(time, signalSamples)
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Continuous Signal Representation')

        # Discrete Signal Representation
        ax2.stem(time, signalSamples)
        ax2.set_xlabel('Sample Index')
        ax2.set_ylabel('Amplitude')
        ax2.set_title('Discrete Signal Representation')

        # Add a title to the entire figure
        fig.suptitle('Graphs')
        # Display the graphs
        plt.show()

    def clearResultLabel(self):
        self.gui.p1_label_result.setText("")

    def openFile(self, guiInput):
        filepath = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File", filetypes=(("Result Files", "*.txt"), ("", "")))
        guiInput.setText(filepath)

    def save_in_file(self, fileName, data):
        # Specify the file path where you want to save the data
        if len(fileName) == 0:
            self.gui.p1_label_result.setText("Error: Please enter file name you want to save")
            return

        fileName += ".txt"

        try:
            with open(fileName, "w") as file:
                file.write(f'{data["signalType"]}\n{data["isPeriodic"]}\n{data["N1"]}\n')

                for item1, item2 in zip(data["firstCoulmn"], data["secondCoulmn"]):
                    file.write(f"{item1} {item2}\n")

            self.gui.p1_label_result.setText("File Saved Successfully.")
        except Exception as e:
            self.gui.p1_label_result.setText(f"Error An error occurred while saving the file: {str(e)}")

    def testResults(self):
        if len(self.gui.p1_lineEdit_filePath.text()) == 0:
            self.gui.p1_label_result.setText("Error: Please Choose Test File")
            return

        if self.gui.p1_tabWidget.currentIndex() == 0:
            self.task1.testResult()
        elif self.gui.p1_tabWidget.currentIndex() == 1:
            self.task2.testResult()
        elif self.gui.p1_tabWidget.currentIndex() == 2:
            self.task3.testResult()
        elif self.gui.p1_tabWidget.currentIndex() == 3:
            self.task4.testResult()
        elif self.gui.p1_tabWidget.currentIndex() == 4:
            self.task5.testResult()
        elif self.gui.p1_tabWidget.currentIndex() == 5:
            self.task6.testResult()
        elif self.gui.p1_tabWidget.currentIndex() == 6:
            self.task7.testResult()
        else:
            self.gui.p1_label_result.setText("Error: This Task not ready yet to test")