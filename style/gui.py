
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from style.design import Ui_MainWindow

class GUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)






class CenteredTextLabel(QWidget):
  def __init__(self, text):
    super().__init__()
    layout = QVBoxLayout()
    label = QLabel(text)
    label.setAlignment(Qt.AlignCenter)
    layout.addWidget(label)
    layout.setContentsMargins(0, 0, 0, 0)
    self.setLayout(layout)