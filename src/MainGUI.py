import sys
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import *
import src.comm.SerialComm as SerialComm
import threading
import time
import queue  # MK: queue를 사용하기 위해 추가
import time  # MK: time을 사용하기 위해 추가
import tkinter  # MK: tkinter(GUI)를 사용하기 위해 추가

main_form = uic.loadUiType("../GUI/Main.ui")[0]
serialPort = SerialComm.SerialPort()


class MainGUI(QMainWindow, main_form):

    def __init__(self, message=None):
        super().__init__()

        self.setupUi(self)
        self.setWindowIcon(QIcon('../GUI/img/icons-motorcycle-01.png'))

        # MAIN Tab
        self.pushBtn_Start.clicked.connect(lambda: self.StartClicked())
        self.pushBtn_Stop.clicked.connect(lambda: self.StopClicked())

        # COMM Tab
        for index in SerialComm.serial_ports():
            self.comboBox_comPort.addItem(index)

        self.btn_PortOpen.clicked.connect(lambda: self.PortOpenClicked())
        self.btn_PortClose.clicked.connect(lambda: self.PortCloseClicked())

        self.btn_Temp_Send.clicked.connect(lambda: self.TempSendClicked())
        self.btn_Humidity_Send.clicked.connect(lambda: self.HumiditySendClicked())
        self.btn_Mortor_Move_Send.clicked.connect(lambda: self.MortorMoveSendClicked())
        self.btn_Mortor_State_Send.clicked.connect(lambda: self.MortorStateSendClicked())

        self.btn_Clear.clicked.connect(lambda: self.ClearClicked())

        serialPort.Open('COM3', 9600)
        serialPort.RegisterReceiveCallback(self.OnReceiveSerialData)

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

    def TempSendClicked(self):
        print('TempSendClicked')
        message = self.textEdit_Temp_Send.toPlainText()
        serialPort.Send(message)
        self.listWidget_Data_Recieve.addItem('TempSendClicked')

    def HumiditySendClicked(self):
        print('HumiditySendClicked')
        message = 'M0'
        serialPort.Send(message)
        self.listWidget_Data_Recieve.addItem('HumiditySendClicked')

    def MortorMoveSendClicked(self):
        print('MortorMoveSendClicked')
        message = 'M0'
        serialPort.Send(message)
        self.listWidget_Data_Recieve.addItem('MortorMoveSendClicked')

    def MortorStateSendClicked(self):
        print('MortorStateSendClicked')
        message = 'M0'
        serialPort.Send(message)
        self.listWidget_Data_Recieve.addItem('MortorStateSendClicked')

    def ClearClicked(self):
        print('ClearClicked')
        self.listWidget_Data_Recieve.addItem('ClearClicked')

    # serial data callback function
    def OnReceiveSerialData(self):
        print("OnReceiveSerialData")
        print(serialPort.receivedMessage)
        self.listWidget_Data_Recieve.addItem(serialPort.receivedMessage)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainGUI()
    mainWindow.show()
    app.exec_()
