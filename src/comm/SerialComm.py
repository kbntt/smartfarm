import glob
import sys
import serial
import _thread
import datetime


def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class SerialPort:
    def __init__(self):
        self.comportName = ""
        self.baud = 0
        self.timeout = None
        self.ReceiveCallback = None
        self.SendCallback = None
        self.isopen = False
        self.receivedMessage = None
        self.serialport = serial.Serial()

    def __del__(self):
        try:
            if self.serialport.is_open():
                self.serialport.close()
        except:
            print("Destructor error closing COM port: ", sys.exc_info()[0])

    def RegisterReceiveCallback(self, aReceiveCallback):
        print('RegisterReceiveCallback')
        self.ReceiveCallback = aReceiveCallback
        try:
            _thread.start_new_thread(self.SerialReadlineThread, ())
        except:
            print("Error starting Read thread: ", sys.exc_info()[0])

    def SerialReadlineThread(self):
        line = []
        while True:

            try:
                if self.serialport.isOpen():
                    # 데이터가 있다면
                    for c in self.serialport.read():
                        # line 변수에 차곡차곡 추가하여 넣는다.
                        line.append(str(chr(c)))
                        if str(chr(c)) == '\r':  # 라인의 끝을 만나면
                            # 데이터 처리 함수로 호출
                            self.receivedMessage = ''.join(line)
                            now = datetime.datetime.now()
                            nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
                            self.ReceiveCallback(nowDatetime+' <=='+self.receivedMessage, self.receivedMessage)
                            # line 변수 초기화
                            del line[:]
                            self.receivedMessage = None
            except:
                print("Error reading COM port: ", sys.exc_info()[0])

    def Open(self, portname, baudrate):
        if not self.serialport.isOpen():
            # serialPort = 'portname', baudrate, bytesize = 8, parity = 'N',
            # stopbits = 1, timeout = None, xonxoff = 0, rtscts = 0)
            self.serialport.port = portname
            self.serialport.baudrate = baudrate
            try:
                self.serialport.open()
                self.isopen = True
            except:
                print("Error opening COM port: ", sys.exc_info()[0])
        else:
            self.isopen = False

    def Close(self):
        if self.isopen:
            try:
                self.serialport.close()
                self.isopen = False
            except:
                print("Close error closing COM port: ", sys.exc_info()[0])
                print("Error opening COM port: ", sys.exc_info()[0])
        else:
            self.isopen = True

    def Send(self, message, aSendCallback):
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')

        self.SendCallback = aSendCallback
        self.SendCallback(nowDatetime + ' =>' + message)

        if self.serialport.isOpen():
            try:
                # Ensure that the end of the message has both \r and \n, not just one or the other
                newmessage = message.strip()
                #newmessage += '\r\n'
                self.serialport.write(newmessage.encode('utf-8'))

            except:
                print("Error sending message: ", sys.exc_info()[0])
            else:
                return True
        else:
            return False
