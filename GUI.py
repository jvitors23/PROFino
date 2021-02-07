from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
import shutil, instrument, monitor, make, os, time, serial

class MainWindow(QMainWindow):
	def __init__(self, filepath, port):
		super(MainWindow, self).__init__()
		self.filepath = filepath
		self.port = port
		# setting title 
		self.setWindowTitle('PROFino') 
		self.resize(600, 350)
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

		self.compileAndUploadBtn = QPushButton("Compile and Upload", self)
		self.compileAndUploadBtn.move(270, 20) 
		self.compileAndUploadBtn.resize(130, 30) 
		self.compileAndUploadBtn.clicked.connect(self.compileAndUpload)	

		self.startProfilingBtn = QPushButton("Start Profiling", self)
		self.startProfilingBtn.move(430, 20) 
		self.startProfilingBtn.resize(100, 30) 
		# self.startProfilingBtn.clicked.connect(self.startProfiling)

		self.logLabel = QLabel("Logs:", self)
		self.logLabel.move(20, 110) 	
		self.logLabel.setFont(lblFont)

		self.logOutput = QTextEdit(self)
		self.logOutput.move(20, 140)
		self.logOutput.resize(560, 100)
		self.logOutput.setReadOnly(True)
		self.logOutput.setLineWrapMode(QTextEdit.NoWrap)
		self.logOutput.setText('')

		font = self.logOutput.font()
		font.setFamily("Courier")
		font.setPointSize(10)

	def compileAndUpload(self): 

		if self.usbPortInput.text() == '' or self.filepath == '':
			self.error_dialog = QErrorMessage(self)
			self.error_dialog.setShortcutEnabled(False)
			self.error_dialog.showMessage('You may input the source file and the USB port.')
		else:
			self.logOutput.setText('Instrumenting...')
			QApplication.processEvents()
			if '/' in self.filepath:
				shutil.copy(self.filepath, './')
				filename = self.filepath.split('/')[-1]
			else:
				filename = self.filepath
			source = filename.split('.')[0] + '.inst' # "arquivo.inst.c"
			functions = instrument.instrument(filename) # Instrumenta o código-fonte original
			self.logOutput.setText('Compiling and uploading to Arduino...')
			QApplication.processEvents()
			ret = make.run(source, self.port) # Compila o código-fonte instrumentado e faz upload para o Arduino
			self.logOutput.setText(ret[0] + ret[1])
		if '/' in self.filepath:
			os.remove(filename)

	def getfile(self):
		file = QFileDialog.getOpenFileName(self, 'Open file', 
				'c:\\',"C files (*.c)")
		if file[0] != '':
			self.filepath = file[0]
			self.fileNameLabel.setText(file[0].split('/')[-1])

def initGUI(filepath, port):
	app = QApplication([])
	mw = MainWindow(filepath, port)
	mw.show()
	app.exec()

