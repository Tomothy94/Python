
import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PyQt5.QtWidgets import QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QAction, qApp



class Notepad(QWidget):

	def __init__(self):
		super().__init__()
		self.savas_btn = QPushButton('Save As')
		self.sav_btn = QPushButton('Save')
		self.opn_btn = QPushButton('Open')
		self.con_btn = QPushButton('Convert')
		self.text = ""

		self.init_ui()

	def init_ui(self):
		v_layout = QVBoxLayout()
		h_layout = QHBoxLayout()

		h_layout.addWidget(self.sav_btn)
		h_layout.addWidget(self.opn_btn)
		h_layout.addWidget(self.con_btn)
		h_layout.addWidget(self.savas_btn)

		v_layout.addLayout(h_layout)

		self.sav_btn.clicked.connect(self.save_text)
		self.opn_btn.clicked.connect(self.open_text)
		self.con_btn.clicked.connect(self.convert_text)
		self.savas_btn.clicked.connect(self.saveas_text)

		self.setLayout(v_layout)
		self.setWindowTitle('PyQt5 TextEdit')

		self.show()

	def save_text(self):
		filename = QFileDialog.getSaveFileName(self, 'Save File', os.getenv('HOME'))
		with open(filename[0], 'w') as f:
			my_text = self.text.toPlainText()
			f.write(my_text)
			
	def saveas_text(self):
		filename = QFileDialog.getSaveFileName(self, 'Save as File', os.getenv('HOME'))
		with open(filename[0], 'w') as f:
			my_text = self.text
			f.write(my_text)		

	def open_text(self):
		filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
		with open(filename[0], 'r') as f:
			file_text = f.read()
			self.text = file_text	
					
	def convert_text(self, dic):
		
		def replace_all(inputText, dic):
			for i, j in dic.items():
				inputText = inputText.replace(i, j)	
			return inputText	
			
		dic = {'Interface':'Port', 'No Shutdown':'Deploy', 'Switchport Access Vlan':'Vlan', 'interface':'port', 'no shutdown':'deploy', 'switchport access vlan':'vlan'}  
		stringToMatch = "Interface"
		
		print ("before " + self.text)	
		self.text = replace_all(self.text, dic)
		print ("after " + self.text)
		#	if stringToMatch in line:
		#		print ("from")
		#		print (line)
		#		line.replace(stringToMatch, stringToReplace)
		#		line = line.replace(line, dic)
		#		lines = [lines.replace('[Interface]', '<int />') for line in lines]
		#		print (line)
			#	lines = line.convert_text(lines, dic)
			#	lines = convert_text(line, dic)
		#	else:
		#		print("This shit is lit")	
		
						
						
		
class Writer(QMainWindow):
	def __init__(self):
		super().__init__()

		self.form_widget = Notepad()
		self.setCentralWidget(self.form_widget)

		self.init_ui()

	def init_ui(self):
		bar = self.menuBar()
		file = bar.addMenu('File')

		new_action = QAction('New-', self)
		new_action.setShortcut('Ctrl+N')

		save_action = QAction('&Save', self)
		save_action.setShortcut('Ctrl+S')

		open_action = QAction('&Open', self)

		quit_action = QAction('&Quit', self)
		
		convert_action = QAction('$Convert', self)

		file.addAction(new_action)
		file.addAction(save_action)
		file.addAction(open_action)
		file.addAction(quit_action)
		file.addAction(convert_action)

		quit_action.triggered.connect(self.quit_trigger)
		file.triggered.connect(self.respond)

		self.show()

	def quit_trigger(self):
		qApp.quit()

	def respond(self, q):
		signal = q.text()

		if signal == '&Open':
			self.form_widget.open_text()
		elif signal == '&Save':
			self.form_widget.save_text()
		elif signal == '$Convert':
			self.form_widget.convert_text()


app = QApplication(sys.argv)
writer = Writer()
sys.exit(app.exec_())