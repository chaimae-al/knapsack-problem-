
#Importing the libraries
import sys
from PyQt5 import QtCore 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer

from PyQt5.QtGui import *
#Creating the main window

class BackPackMainWindow(QMainWindow):
	#Defining the constructor 
	def __init__(self):
		super().__init__()

		self.items = []
		self.capacity = 0
		self.algorithm = 'Dynamic Programming'
		
		self.setWindowTitle("BackPack Problem Solver")
		self.setGeometry(100, 100, 800, 600)

		self.initUI()

	#Defining the widgets
	def initUI(self):
		# Creating the central widget
		central_widget = QWidget()
		self.setCentralWidget(central_widget)
		layout = QVBoxLayout()

		#Input sections
		input_layout = QHBoxLayout()

		#Creating the 3 essential iputs
		self.weight_input = QLineEdit()
		self.value_input = QLineEdit()
		self.capacity_input = QLineEdit()

		#Creation the lables for the inputs and adding them to the layout
			#//label for the weight
		input_layout.addWidget(QLabel("Weight:"))
		input_layout.addWidget(self.weight_input)
			#//label for the value
		input_layout.addWidget(QLabel("Value:"))
		input_layout.addWidget(self.value_input)
			#//label for the capacity
		input_layout.addWidget(QLabel("Capacity:"))
		input_layout.addWidget(self.capacity_input)

		#Creating the buttons and adding them to the layout		 
			#//Creating the add button
		add_item_button = QPushButton("Add Item")
			#//Creating the import button
		import_button = QPushButton("Import")
		input_layout.addWidget(add_item_button)
		input_layout.addWidget(import_button)
		
		#Adding the inputs to the layout
		layout.addLayout(input_layout)

		#Connecting the buttons to the functions
		add_item_button.clicked.connect(self.add_item)
		import_button.clicked.connect(self.import_data)

		#Adding the visualization area in which will the objects be displayed 
		self.visualization_area = QGraphicsView()
		self.scene = QGraphicsScene()
		self.visualization_area.setScene(self.scene)
		layout.addWidget(self.visualization_area)

		#Creating the control buttons
		control_layout = QHBoxLayout()
			#//Creating the solve button
		solve_button = QPushButton("Solve")
			#//Creating the clear button
		reset_button = QPushButton("reset")
		#Adding the buttons to the control layout
		control_layout.addWidget(solve_button)
		control_layout.addWidget(reset_button)
		#Adding the control layout to the main layout
		layout.addLayout(control_layout)

		#Connecting the buttons to the functions
		solve_button.clicked.connect(self.solve_problem)
		reset_button.clicked.connect(self.reset)

		
		# Solution display
		self.solution_text = QTextEdit()
		self.solution_text.setFont(QFont('Times',16))
		#Adding the solution text to the layout
		layout.addWidget(self.solution_text)
		

		#the layout to the central widget
		central_widget.setLayout(layout)

		
        # Animation Timer
		self.timer = QTimer()
		self.timer.timeout.connect(self.update_animation)
		self.animation_index = 0

		#Creating the export Button
		export_button = QPushButton("Export")
		control_layout.addWidget(export_button)
		export_button.clicked.connect(self.export)
		

	#Defining the function to add an item
	def add_item(self):
		try:
			weight = int(self.weight_input.text())
			value = int(self.value_input.text())
			self.items.append((weight, value))
			self.weight_input.clear()
			self.value_input.clear()
			self.update_visualization()
			
		except ValueError:
			self.solution_text.setText("Please enter valid integers for weight and value.")

	#Defining the import function 
	def import_data(self):
		file_path = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)')[0]
		if file_path:
			with open(file_path, 'r') as file:
				lines = file.readlines()
				self.items = []
				for line in lines:
					weight, value = map(int, line.split())
					self.items.append((weight, value))
				self.update_visualization()

	#Defining the update visualisation function
	def update_visualization(self):
		self.scene.clear()
		x = 10
		for weight, value in self.items:
			item_rect = QGraphicsRectItem(x, 10, 50, 50)
			item_rect.setBrush(QColor(135, 206, 235))
			self.scene.addItem(item_rect)
			weight_text = self.scene.addText(f"W : {weight}")
			weight_text.setFont(QFont('Times',9))
			weight_text.setPos(x + 5, 15)
			value_text = self.scene.addText(f"V : {value}")
			value_text.setFont(QFont('Times',9))
			value_text.setPos(x + 5, 35)
			x += 60

	#Defining the solve function
	def solve_problem(self):
		try:
			self.capacity = int(self.capacity_input.text())
			n = len(self.items)
			if n == 0 or self.capacity == 0:
				self.solution_text.setText("Please add items and set capacity.")
				return
			self.algorithm_solution()
		except ValueError:
			self.solution_text.setText("Please enter a valid integer for capacity.")

	#Defining the algorithm function
	def algorithm_solution(self):
		items = sorted([(v/w, w, v, i) for i, (w, v) in enumerate(self.items)], reverse=True)
		total_value = 0
		total_weight = 0
		selected_items = []
		
		for ratio, weight, value, index in items:
			if total_weight + weight <= self.capacity:
				total_weight += weight
				total_value += value
				selected_items.append(index)
			else:
				break
		self.animate_solution(selected_items, [item[0] for item in self.items], [item[1] for item in self.items])

	#Defining the animate function taht animates the result
	def animate_solution(self, selected_items, weights, values):
		self.solution_text.clear()
		self.solution_text.append("Animating solution...")
		self.selected_items = selected_items
		self.animation_index = 0
		self.timer.start(500)  # Adjust the timer interval for animation speed
	
	#Defining the update animation function
	
	def update_animation(self):
		if self.animation_index < len(self.selected_items):
			index = self.selected_items[self.animation_index]
			weight, value = self.items[index]
			item_rect = QGraphicsRectItem(10 + index * 60, 10, 50, 50)
			item_rect.setBrush(Qt.green)
			self.scene.addItem(item_rect)
			weight_text = self.scene.addText(f"W: {weight}")
			weight_text.setPos(15 + index * 60, 15)
			value_text = self.scene.addText(f"V: {value}")
			value_text.setPos(15 + index * 60, 35)
			self.animation_index += 1
		else:
			self.timer.stop()
			self.display_solution(self.selected_items)

	#Defining the display function
	def display_solution(self, selected_items):
		self.solution_text.clear()
		total_weight = 0
		total_value = 0
		self.solution_text.append("Selected items:")
		for i in selected_items:
			weight, value = self.items[i]
			total_weight += weight
			total_value += value
			self.solution_text.append(f"Item {i+1} - Weight: {weight}, Value: {value}")
			self.solution_text.append(f"\nTotal Weight: {total_weight}")
		self.solution_text.append(f"Total Value: {total_value}")

	#Defining the reset function
	def reset(self):
		self.items = []
		self.capacity = 0
		self.weight_input.clear()
		self.value_input.clear()
		self.capacity_input.clear()
		self.solution_text.clear()
		self.scene.clear()

	#Defining the export function
	def export(self):
		file_path = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;All Files (*)')[0]
		if file_path:
			with open(file_path, 'w') as file:
				file.write(self.solution_text.toPlainText())

#The main function to run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = BackPackMainWindow()
    mainWin.show()
    sys.exit(app.exec_())
