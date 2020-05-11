from PyQt5 import QtGui, QtCore

app = QtGui.QApplication([])
app.setStyleSheet('QMainWindow{background-color: darkgray;border: 1px solid black;}')

w = QtGui.QMainWindow()
w.setWindowFlags(QtCore.Qt.FramelessWindowHint)
w.show()

app.exec_()