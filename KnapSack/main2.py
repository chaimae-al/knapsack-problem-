import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer

# Creating the main window
class KnapsackGUI(QMainWindow):
    # the constructor for the main window
    def __init__(self):
        super().__init__()

        self.items = []
        self.capacity = 0
        self.algorithm = 'Dynamic Programming'
        
        self.setWindowTitle("Knapsack Problem Solver")
        self.setGeometry(100, 100, 800, 600)

        self.initUI()
	# Defining the widgets
    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Input sections
        input_layout = QHBoxLayout()
			#weight input 
        self.weight_input = QLineEdit()
			#value input 
        self.value_input = QLineEdit()
        	#capacity input 
        self.capacity_input = QLineEdit()
			#add item button
        add_item_button = QPushButton("Add Item")
			#import button
        import_button = QPushButton("Import Data")
		#the labels for the inputs
			#the weight label
        input_layout.addWidget(QLabel("Weight:"))
			#the value weight_input
        input_layout.addWidget(self.weight_input)
			#the value label
        input_layout.addWidget(QLabel("Value:"))
			#the content  of the value
        input_layout.addWidget(self.value_input)
        input_layout.addWidget(QLabel("Capacity:"))
        input_layout.addWidget(self.capacity_input)
			#the add button 
        input_layout.addWidget(add_item_button)
        	#the import button 
        input_layout.addWidget(import_button)
        
        layout.addLayout(input_layout)

        add_item_button.clicked.connect(self.add_item)
        import_button.clicked.connect(self.import_data)

        # # Algorithm selection
        # algo_layout = QHBoxLayout()
        # self.algo_combo = QComboBox()
        # self.algo_combo.addItems(['Dynamic Programming', 'Greedy Algorithm'])
        # algo_layout.addWidget(QLabel("Algorithm:"))
        # algo_layout.addWidget(self.algo_combo)
        # layout.addLayout(algo_layout)

        # self.algo_combo.currentTextChanged.connect(self.update_algorithm)

        # Visualization section
        self.visualization_area = QGraphicsView()
        self.scene = QGraphicsScene()
        self.visualization_area.setScene(self.scene)
        layout.addWidget(self.visualization_area)

        # Solution display
        self.solution_text = QTextEdit()
        layout.addWidget(self.solution_text)

        # Control buttons
        control_layout = QHBoxLayout()
        solve_button = QPushButton("Solve")
        reset_button = QPushButton("Reset")
        export_button = QPushButton("Export")
        control_layout.addWidget(solve_button)
        control_layout.addWidget(reset_button)
        control_layout.addWidget(export_button)
        layout.addLayout(control_layout)

        solve_button.clicked.connect(self.solve_knapsack)
        reset_button.clicked.connect(self.reset)
        export_button.clicked.connect(self.export_solution)

        	

        # Animation Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.animation_index = 0

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

    def update_visualization(self):
        self.scene.clear()
        x = 10
        for weight, value in self.items:
            item_rect = QGraphicsRectItem(x, 10, 50, 50)
            item_rect.setBrush(Qt.blue)
            self.scene.addItem(item_rect)
            weight_text = self.scene.addText(f"W: {weight}")
            weight_text.setPos(x + 5, 15)
            value_text = self.scene.addText(f"V: {value}")
            value_text.setPos(x + 5, 35)
            x += 60

    def update_algorithm(self, text):
        self.algorithm = text


	# The algorithm for solving the knapsack problem
    def solve_knapsack(self):
        try:
            self.capacity = int(self.capacity_input.text())
            n = len(self.items)
            if n == 0 or self.capacity == 0:
                self.solution_text.setText("Please add items and set capacity.")
                return

            # if self.algorithm == 'Dynamic Programming':
            #     self.dynamic_programming_solution()
            # elif self.algorithm == 'Greedy Algorithm':
                # self.greedy_algorithm_solution()
            self.greedy_algorithm_solution()
        except ValueError:
            self.solution_text.setText("Please enter a valid integer for capacity.")

    # def dynamic_programming_solution(self):
    #     weights = [item[0] for item in self.items]
    #     values = [item[1] for item in self.items]
    #     n = len(weights)
    #     dp = [[0 for _ in range(self.capacity + 1)] for _ in range(n + 1)]

    #     for i in range(1, n + 1):
    #         for w in range(1, self.capacity + 1):
    #             if weights[i-1] <= w:
    #                 dp[i][w] = max(values[i-1] + dp[i-1][w-weights[i-1]], dp[i-1][w])
    #             else:
    #                 dp[i][w] = dp[i-1][w]

    #     result = dp[n][self.capacity]
    #     selected_items = []
    #     w = self.capacity
    #     for i in range(n, 0, -1):
    #         if result <= 0:
    #             break
    #         if result == dp[i-1][w]:
    #             continue
    #         else:
    #             selected_items.append(i-1)
    #             result -= values[i-1]
    #             w -= weights[i-1]

    #     self.animate_solution(selected_items, weights, values)

    def greedy_algorithm_solution(self):
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

    def animate_solution(self, selected_items, weights, values):
        self.solution_text.clear()
        self.solution_text.append("Animating solution...")
        self.selected_items = selected_items
        self.animation_index = 0
        self.timer.start(500)  # Adjust the timer interval for animation speed

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

    def reset(self):
        self.items = []
        self.capacity = 0
        self.weight_input.clear()
        self.value_input.clear()
        self.capacity_input.clear()
        self.solution_text.clear()
        self.scene.clear()

    def export_solution(self):
        file_path = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;All Files (*)')[0]
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.solution_text.toPlainText())
                


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = KnapsackGUI()
    mainWin.show()
    sys.exit(app.exec_())
