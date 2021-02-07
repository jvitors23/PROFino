from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import shutil
import instrument
import monitor
import make
import os
import time
import serial
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.ticker as ticker


class MainWindow(QMainWindow):
    def __init__(self, filepath, port):
        super(MainWindow, self).__init__()
        self.filepath = filepath
        self.port = port

        self.stop = False
        self.timestamp = 0
        self.func_monitor = {}

        # setting title
        self.setWindowTitle('PROFino')
        self.setFixedSize(600, 380)

        # calling method
        self.UiComponents()

    # method for widgets
    def UiComponents(self):

        lblFont = QFont()
        lblFont.setBold(True)

        self.usbPortInput = QLineEdit(self.port, self)
        self.usbPortInput.move(100, 20)
        self.usbPortInput.resize(100, 30)

        # Label usb Port
        self.usbLabel = QLabel("USB Port: ", self)
        self.usbLabel.move(20, 20)
        self.usbLabel.setFont(lblFont)

        # select File Button
        self.selectFileBtn = QPushButton("", self)
        btnIcon = QIcon('assets/fileicon.png')
        self.selectFileBtn.setIcon(btnIcon)
        self.selectFileBtn.move(100, 70)
        self.selectFileBtn.resize(100, 30)
        self.selectFileBtn.clicked.connect(self.getfile)

        self.selectFileLabel = QLabel("Select File:", self)
        self.selectFileLabel.move(20, 70)
        self.selectFileLabel.setFont(lblFont)

        if self.filepath == '':
            self.fileNameLabel = QLabel("", self)
        else:
            if '/' in self.filepath:
                self.fileNameLabel = QLabel(self.filepath.split('/')[-1], self)
            else:
                QLabel(self.filepath, self)
        self.fileNameLabel.move(270, 70)

        self.compileAndUploadBtn = QPushButton("Build and Upload", self)
        self.compileAndUploadBtn.move(270, 20)
        self.compileAndUploadBtn.resize(130, 30)
        self.compileAndUploadBtn.clicked.connect(self.buildAndUpload)

        self.startProfilingBtn = QPushButton("Start Profiling", self)
        self.startProfilingBtn.move(470, 20)
        self.startProfilingBtn.resize(100, 30)
        self.startProfilingBtn.setDisabled(True)
        self.startProfilingBtn.clicked.connect(self.startProfiling)

        self.stopProfilingBtn = QPushButton("Stop Profiling", self)
        self.stopProfilingBtn.move(470, 70)
        self.stopProfilingBtn.setDisabled(True)
        self.stopProfilingBtn.resize(100, 30)
        self.stopProfilingBtn.clicked.connect(self.stopProfiling)

        self.logLabel = QLabel("Logs:", self)
        self.logLabel.move(20, 110)
        self.logLabel.setFont(lblFont)

        self.errorLabel = QLabel("", self)
        self.errorLabel.move(270, 110)
        self.errorLabel.resize(270, 20)
        self.errorLabel.setStyleSheet('color: red')

        self.logOutput = QTextEdit(self)
        self.logOutput.move(20, 140)
        font = QFont("Courier")
        font.setBold(True)
        self.logOutput.resize(560, 220)
        self.logOutput.setReadOnly(True)
        self.logOutput.setFont(font)
        self.logOutput.setLineWrapMode(QTextEdit.NoWrap)
        self.logOutput.setText('')

    def buildAndUpload(self):
        self.func_monitor = {}
        if self.usbPortInput.text() == '' or self.filepath == '':
            self.error_dialog = QErrorMessage(self)
            self.error_dialog.setShortcutEnabled(False)
            self.error_dialog.showMessage(
                'You need to input the source file and the USB port.')
        else:
            self.errorLabel.setText("")
            self.startProfilingBtn.setDisabled(True)
            self.logOutput.setText('Instrumenting...')
            QApplication.processEvents()
            if '/' in self.filepath:
                shutil.copy(self.filepath, './')
                filename = self.filepath.split('/')[-1]
            else:
                filename = self.filepath
            self.port = self.usbPortInput.text()
            source = filename.split('.')[0] + '.inst'  # "arquivo.inst.c"
            # Instrumenta o código-fonte original
            self.functions = instrument.instrument(filename)
            self.logOutput.setText('Compiling and uploading to Arduino...')
            QApplication.processEvents()
            # Compila o código-fonte instrumentado e faz upload para o Arduino
            ret = make.run(source, self.port)
            if 'Error' in ret[0] or 'Error' in ret[1]:
                self.errorLabel.setText(
                    "Error while building or uploading to Arduino!")
                self.startProfilingBtn.setDisabled(True)
                QApplication.processEvents()
            else:
                self.startProfilingBtn.setDisabled(False)
                QApplication.processEvents()
            self.logOutput.setText(ret[0] + ret[1])
            if '/' in self.filepath:
                os.remove(filename)

    def startProfiling(self):
        self.stop = False
        self.func_monitor = {}
        self.startProfilingBtn.setDisabled(True)
        self.stopProfilingBtn.setDisabled(False)
        self.logOutput.setText('Starting Profiling...')
        QApplication.processEvents()

        try:
            arduino = serial.Serial(self.port, timeout=1)
            arduino.flushInput()
            arduino.flushOutput()
        except:
            self.logOutput.append('Please check the port')
            QApplication.processEvents()

        call_stack = []
        self.func_monitor = {}
        iniCount = 0
        self.timestamp = 0
        start = False
        end = False
        ini_interval = 0

        for func in self.functions:
            self.func_monitor[func['name']] = {
                'calls': 0,
                'time': 0,
                'percentage': 0
            }

        while True:
            if self.stop:
                break
            rawdata = []
            rawdata.append(str(arduino.readline()))
            msg = monitor.clean(rawdata)[0]
            if msg != '' and len(msg.split(':')) > 1 and msg.split(':')[1] == 'inicio':
                iniCount += 1
            if iniCount == 3 and not start:
                ini_interval = time.time()
                start = True
                continue

            if start and msg != '':
                overflow = int(msg.split(":")[1])
                overflow_counter = int(msg.split(":")[2])
                func_name = msg.split(":")[3]
                tipo = int(msg.split(":")[4])
                self.timestamp = overflow_counter*32000*4.096/1000 + overflow*4.096/1000
                if tipo == 1:
                    self.func_monitor[func_name]['calls'] += 1
                    if func_name != 'main':
                        self.func_monitor[call_stack[-1][0]
                                          ]['time'] += (self.timestamp - call_stack[-1][1])
                    call_stack.append([func_name, self.timestamp])
                else:
                    last_func_entry = call_stack.pop()
                    # o tempo de entrada da função anterior passa a ser o atual
                    if func_name != 'main':
                        call_stack[-1][1] = self.timestamp
                    else:
                        end = True
                    self.func_monitor[func_name]['time'] += (
                        self.timestamp - last_func_entry[1])

            if start and (time.time() - ini_interval) >= 0.5:
                self.logOutput.setText("")
                print_list = []
                maior = 0
                for func in self.func_monitor.keys():
                    if len(func) > maior:
                        maior = len(func)
                    print_list.append([func, str(self.func_monitor[func]['calls']), str(self.func_monitor[func]['time'])[
                                      0:8], str((self.func_monitor[func]['time']/self.timestamp)*100)[0:8]])
                    self.func_monitor[func]['percentage'] = (
                        self.func_monitor[func]['time']/self.timestamp)*100

                self.logOutput.append(
                    '====================================================================')
                self.logOutput.append('{0:<{1}}{2:<20}{3:<20}{4:<20}'.format(
                    'function', maior + 10, 'calls', 'time (s)', 'time(%)'))
                self.logOutput.append(
                    '--------------------------------------------------------------------')

                for func in print_list:
                    self.logOutput.append('{0:<{1}}{2:<20}{3:<20}{4:<20}'.format(
                        func[0], maior + 10, func[1], func[2], func[3]))

                ini_interval = time.time()
                self.logOutput.append(
                    '--------------------------------------------------------------------')
                self.logOutput.append(
                    'total execution time (s) ' + str(self.timestamp)[0:8])
                self.logOutput.append(
                    '====================================================================')
                QApplication.processEvents()

                if end:
                    self.logOutput.append('program finished')
                    self.stopProfilingBtn.setDisabled(True)
                    self.startProfilingBtn.setDisabled(False)
                    QApplication.processEvents()
                    self.displayGraph()
                    break

    def stopProfiling(self):
        self.stop = True
        self.logOutput.append('Profiling stopped')
        self.stopProfilingBtn.setDisabled(True)
        self.startProfilingBtn.setDisabled(False)
        QApplication.processEvents()
        self.displayGraph()

    def displayGraph(self):
        bar_width = 0.5
        time, percentage = [], []
        funcs = self.func_monitor.keys()

        for f in self.func_monitor.keys():
            percentage.append(self.func_monitor[f]['percentage'])
            time.append(self.func_monitor[f]['time'])

        fig, ax = plt.subplots()
        bars = ax.bar(funcs, time, bar_width)
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

        for i, bar in enumerate(bars):
            ax.text(bar.get_x() + bar_width/2.0, bar.get_height(),
                    '{:.2f}%'.format(percentage[i]), ha='center', va='bottom')

        plt.xlabel('Functions')
        plt.ylabel('Elapsed Time (s)')
        plt.show()

    def getfile(self):
        file = QFileDialog.getOpenFileName(self, 'Open file',
                                           'c:\\', "C files (*.c)")
        if file[0] != '':
            self.filepath = file[0]
            self.fileNameLabel.setText(file[0].split('/')[-1])


def initGUI(filepath, port):
    app = QApplication([])
    mw = MainWindow(filepath, port)
    mw.show()
    app.exec()
