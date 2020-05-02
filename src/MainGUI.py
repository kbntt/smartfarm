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
        """
        self.btn_PortOpen.connect(lambda: self.PortOpenClicked())
        self.btn_PortClose.connect(lambda: self.PortCloseClicked())
        self.btn_DataSend.connect(lambda: self.DataSendClicked())
        self.btn_Clear.connect(lambda: self.ClearClicked())
        """

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
        model = QStandardItemModel(self)
        model.appendRow("PortOpenClicked")
        self.listView_Data_Recieve.setModel(model)

    
    def PortCloseClicked(self):
        print('PortCloseClicked')
        model = QStandardItemModel(self)
        model.appendRow("PortCloseClicked")
        self.listView_Data_Recieve.setModel(model)

    def DataSendClicked(self):
        print('DataSendClicked')
        model = QStandardItemModel(self)
        model.appendRow("DataSendClicked")
        self.listView_Data_Recieve.setModel(model)

    def ClearClicked(self):
        print('ClearClicked')
        model = QStandardItemModel(self)
        model.appendRow("ClearClicked")
        self.listView_Data_Recieve.setModel(model)
    """


if __name__ == '__main__':
    # Serial 통신
    app = QApplication(sys.argv)
    mainWindow = MainGUI()
    mainWindow.show()
    app.exec_()
