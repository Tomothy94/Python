
import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QWidget
from PyQt5.QtWidgets import QTextEdit, QPushButton, QVBoxLayout, QHBoxLayout, QAction, qApp, QLabel, QComboBox



class Notepad(QWidget):

	def __init__(self):
		super().__init__()
		self.opn_btn = QPushButton('Open')
		self.con_btn = QPushButton('Convert')
		self.con_comb = QComboBox()
		self.con_comb.addItem('Cisco to Brocade')
		self.con_comb.addItem('Brocade to Cisco')		
		
		self.filepath_lbl = QLabel('Select a file...')
		self.text = ""

		self.init_ui()

	def init_ui(self):
		v_layout = QVBoxLayout()
		h_filepath = QHBoxLayout()
		h_convert = QHBoxLayout()

		h_filepath.addWidget(self.opn_btn)
		h_filepath.addWidget(self.filepath_lbl)
		h_convert.addWidget(self.con_comb)
		h_convert.addWidget(self.con_btn)

		v_layout.addLayout(h_filepath)
		v_layout.addLayout(h_convert)

		self.opn_btn.clicked.connect(self.open_text)
		self.con_btn.clicked.connect(self.convert_text)

		self.setLayout(v_layout)
		self.setWindowTitle('PyQt5 TextEdit')

		self.show()
			
	def saveas_text(self):
		filename = QFileDialog.getSaveFileName(self, 'Save as File', os.getenv('HOME'))
		with open(filename[0], 'w') as f:
			my_text = self.text
			f.write(my_text)		

	def open_text(self):
		filename = QFileDialog.getOpenFileName(self, 'Open File', os.getenv('HOME'))
		self.filepath_lbl.setText(filename[0])
		
		with open(filename[0], 'r') as f:
			file_text = f.read()
			self.text = file_text	
					
	def convert_text(self, dic):
		
		def replace_all(inputText, dic):
			for i, j in dic.items():
				inputText = inputText.replace(i, j)	
			return inputText	
			
		ciscoDictionary = {'Interface':'Port', 'No Shutdown':'Deploy', 'Switchport Access Vlan':'Vlan', 'interface':'port', 'no shutdown':'deploy', 'switchport access vlan':'vlan'}  
		brocadeDictionary = {'Port':'Interface', 'Deploy':'No Shutdown', 'Vlan':'Switchport Access Vlan',  'deploy':'no shutdown', 'vlan':'switchport access vlan'}
		
		stringToMatch = "Interface"
		
		if(self.con_comb.currentText() == 'Cisco to Brocade'):
			self.text = replace_all(self.text, ciscoDictionary)
		elif(self.con_comb.currentText() == 'Brocade to Cisco'):
			self.text = replace_all(self.text, brocadeDictionary)
			
		self.saveas_text()
		sys.exit()
		
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