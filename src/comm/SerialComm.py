import glob
import sys
import serial
import _thread
import time

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
        self.isopen = False
        self.receivedMessage = None
        self.serialport = serial.Serial()
        #self.serialport = serial.Serial('COM3', 9600)

        print('__init__')

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
        print('SerialReadlineThread')
        while True:
            #print("receivedMessage 1")
            try:
                #print("receivedMessage 2")
                if self.isopen:

                    # 데이터가 있있다면
                    for c in self.serialport.read():
                        # line 변수에 차곡차곡 추가하여 넣는다.
                        #print("chr(c)", chr(c))
                        line.append(str(chr(c)))

                        if str(chr(c)) == '\r':  # 라인의 끝을 만나면
                            # 데이터 처리 함수로 호출
                            print("22222")
                            # print(line)
                            print(''.join(line))
                            self.receivedMessage = ''.join(line)
                            print("self.receivedMessage", self.receivedMessage)
                            if self.receivedMessage != "":
                                self.ReceiveCallback()
                            # line 변수 초기화
                            del line[:]
                            self.receivedMessage = None
                            # print("44444")

                    """
                    self.receivedMessage = self.serialport.readline()
                    print("receivedMessage")
                    print(self.serialport.readline())
                    if self.receivedMessage != "":
                        self.ReceiveCallback(self.receivedMessage)
                        """
            except:
                print("Error reading COM port: ", sys.exc_info()[0])

    def IsOpen(self):
        return self.isopen

    def Open(self, portname, baudrate):
        if not self.isopen:
            # serialPort = 'portname', baudrate, bytesize = 8, parity = 'N',
            # stopbits = 1, timeout = None, xonxoff = 0, rtscts = 0)
            self.serialport.port = portname
            self.serialport.baudrate = baudrate
            try:
                self.serialport.open()
                self.isopen = True
            except:
                print("Error opening COM port: ", sys.exc_info()[0])

    def Close(self):
        if self.isopen:
            try:
                self.serialport.close()
                self.isopen = False
            except:
                print("Close error closing COM port: ", sys.exc_info()[0])

    def Send(self, message):
        print('Send', self.isopen)
        print('message', message)
        if self.isopen:
            try:
                # Ensure that the end of the message has both \r and \n, not just one or the other

                newmessage = message.strip()
                newmessage += '\r\n'
                self.serialport.write(newmessage.encode('utf-8'))
                """
                print("Send:", str.encode('M0'))
                self.serialport.write(str.encode('M0'))
                """
            except:
                print("Error sending message: ", sys.exc_info()[0])
            else:
                return True
        else:
            return False

    # 데이터 처리할 함수
    def parsing_data(data):
        # 리스트 구조로 들어 왔기 때문에
        # 작업하기 편하게 스트링으로 합침
        print(data)
        print(type(data))
        tmp = ''.join(data)
        print(tmp)