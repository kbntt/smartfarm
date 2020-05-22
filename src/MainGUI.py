import sys
import cv2
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp
import src.comm.SerialComm as SerialComm
import threading
import time
import src.comm.Variable as Var

main_form = uic.loadUiType("../GUI/Main.ui")[0]
serialPort = SerialComm.SerialPort()

class MainGUI(QMainWindow, main_form):

    def __init__(self, message=None):

        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('../GUI/img/icons-motorcycle-01.png'))
        self.initMenuBarUI()
        self.initMainTabUI()
        self.initCOMMTabUI()
        self.initStatusBarUI()

        serialPort.RegisterReceiveCallback(self.OnReceiveSerialData)
        t1 = threading.Thread(target=self.MainRhread, args=())
        t1.start()

        t2 = threading.Thread(target=self.videoRhread, args=())
        t2.start()

    def initMenuBarUI(self):
        exitAction = QAction(QIcon('../GUI/img/icon_exit_01.png'), '종료', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(exitAction)

    def initMainTabUI(self):

        # MAIN Tab
        self.pushBtn_Start.clicked.connect(lambda: self.StartClicked())
        self.pushBtn_Stop.clicked.connect(lambda: self.StopClicked())

    def initCOMMTabUI(self):

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

    def initStatusBarUI(self):
        self.statusBar().showMessage('Ready')

    def MainRhread(self):
        while True:
            time.sleep(0.05)
            self.UIUpdate()

    def videoRhread(self):

        cap = cv2.VideoCapture('test.avi')
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.lbl_video.resize(width, height)
        while True:
            ret, img = cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                self.lbl_video.setPixmap(pixmap)
            else:
                QtWidgets.QMessageBox.about(mainWindow, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break
        cap.release()
        print("Thread end.")

    # MAIN Tab
    def StartClicked(self):
        print('StartClicked')
        self.lineEdit_CurrTemp.setText('StartClicked')

    def StopClicked(self):
        print('StopClicked')
        self.lineEdit_Humidity.setText('StartClicked')

    # COMM Tab

    def PortOpenClicked(self):
        serialPort.Open(self.comboBox_comPort.currentText(), int(self.comboBox_BaudRate.currentText()))
        print('PortOpenClicked')

    def PortCloseClicked(self):
        print('PortCloseClicked')
        serialPort.Close()

    def TempSendClicked(self):
        message = self.textEdit_Temp_Send.toPlainText()
        serialPort.Send(message, self.OnSendSerialData)

    def HumiditySendClicked(self):
        message = self.textEdit_Humidity_Send.toPlainText()
        serialPort.Send(message, self.OnSendSerialData)

    def MortorMoveSendClicked(self):
        message = self.textEdit_Mortor_Move_Send.toPlainText()
        serialPort.Send(message, self.OnSendSerialData)

    def MortorStateSendClicked(self):
        message = self.textEdit_Mortor_State_Send.toPlainText()
        serialPort.Send(message, self.OnSendSerialData)

    def ClearClicked(self):
        self.listWidget_Data_Recieve.clear()

    # SerialComm 콜백함수
    def OnReceiveSerialData(self, receivedMessage):
        self.listWidget_Data_Recieve.addItem(receivedMessage)

    # SerialComm 콜백함수
    def OnSendSerialData(self, sendMessage):
        self.listWidget_Data_Recieve.addItem(sendMessage)

    # 화면 업데이트
    def UIUpdate(self):
        if serialPort.isopen:
            self.btn_PortOpen.setStyleSheet(Var.BTN_ON_COLOER)
            self.btn_PortClose.setStyleSheet(Var.BTN_OFF_COLOER)
            self.btn_PortOpen.setDisabled(True)
            self.btn_PortClose.setEnabled(True)
        else:
            self.btn_PortOpen.setStyleSheet(Var.BTN_OFF_COLOER)
            self.btn_PortClose.setStyleSheet(Var.BTN_ON_COLOER)
            self.btn_PortClose.setDisabled(True)
            self.btn_PortOpen.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainGUI()
    mainWindow.show()
    app.exec_()
