import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QIcon

main_form = uic.loadUiType("../GUI/Main.ui")[0]


class MainGUI(QMainWindow, main_form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushBtn_Start.clicked.connect(lambda: self.StartClicked())
        self.pushBtn_Stop.clicked.connect(lambda: self.StopClicked())
        self.setWindowIcon(QIcon('../GUI/img/icons-motorcycle-01.png'))

    def StartClicked(self):
        print('StartClicked')
        self.lineEdit_CurrTemp.setText('StartClicked')

    def StopClicked(self):
        print('StopClicked')
        self.lineEdit_Humidity.setText('StartClicked')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainGUI()
    mainWindow.show()
    app.exec_()
