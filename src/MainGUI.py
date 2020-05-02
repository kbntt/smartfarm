import sys
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import *
import src.comm.SerialComm as SerialComm

main_form = uic.loadUiType("../GUI/Main.ui")[0]


class MainGUI(QMainWindow, main_form):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowIcon(QIcon('../GUI/img/icons-motorcycle-01.png'))

        # MAIN Tab
        self.pushBtn_Start.clicked.connect(lambda: self.StartClicked())
        self.pushBtn_Stop.clicked.connect(lambda: self.StopClicked())

        # COMM Tab
        for i in SerialComm.serial_ports():
            self.comboBox_comPort.addItem(i)

        self.btn_PortOpen.clicked.connect(lambda: self.PortOpenClicked())
        self.btn_PortClose.clicked.connect(lambda: self.PortCloseClicked())
        self.btn_DataSend.clicked.connect(lambda: self.DataSendClicked())
        self.btn_Clear.clicked.connect(lambda: self.ClearClicked())

    # MAIN Tab
    def StartClicked(self):
        print('StartClicked')
        self.lineEdit_CurrTemp.setText('StartClicked')

    def StopClicked(self):
        print('StopClicked')
        self.lineEdit_Humidity.setText('StartClicked')

    # COMM Tab

    def PortOpenClicked(self):
        print('PortOpenClicked')
        self.listWidget_Data_Recieve.addItem('PortOpenClicked')


    def PortCloseClicked(self):
        print('PortCloseClicked')
        self.listWidget_Data_Recieve.addItem('PortCloseClicked')

    def DataSendClicked(self):
        print('DataSendClicked')
        self.listWidget_Data_Recieve.addItem('DataSendClicked')

    def ClearClicked(self):
        print('ClearClicked')
        self.listWidget_Data_Recieve.addItem('ClearClicked')


if __name__ == '__main__':
    # Serial 통신
    app = QApplication(sys.argv)
    mainWindow = MainGUI()
    mainWindow.show()
    app.exec_()
