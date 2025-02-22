# game_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QFont
import random
from results_window import ResultsWindow
from data_manager import DataManager

class GameWindow(QWidget):
    def __init__(self, time, ranges):
        super().__init__()
        self.time_left = time
        self.start_time = time
        self.ranges = ranges
        self.score = 0
        self.questions_asked = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.initUI()
        self.new_question()
        self.timer.start(1000)
        self.data_manager = DataManager()

    def initUI(self):
        self.setWindowTitle('Arithmetic Game')
        self.setGeometry(300, 300, 400, 300)
        
        layout = QVBoxLayout()
        
        self.question_label = QLabel('', self)
        self.question_label.setAlignment(Qt.AlignCenter)
        self.question_label.setFont(QFont('Arial', 24))
        layout.addWidget(self.question_label)
        
        self.answer_input = QLineEdit(self)
        self.answer_input.setAlignment(Qt.AlignCenter)
        self.answer_input.setFont(QFont('Arial', 18))
        self.answer_input.returnPressed.connect(self.check_answer)
        layout.addWidget(self.answer_input)
        
        self.score_label = QLabel('Score: 0', self)
        self.score_label.setAlignment(Qt.AlignCenter)
        self.score_label.setFont(QFont('Arial', 18))
        layout.addWidget(self.score_label)
        
        self.time_label = QLabel(f'Time: {self.time_left}', self)
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setFont(QFont('Arial', 18))
        layout.addWidget(self.time_label)
        
        self.setLayout(layout)

    def new_question(self):
        operations = list(self.ranges.keys())
        operation = random.choice(operations)
        
        term1_range = self.ranges[operation]['term1']
        term2_range = self.ranges[operation]['term2']
        
        if operation in ['+', '-']:
            a = random.randint(term1_range['min'], term1_range['max'])
            b = random.randint(term2_range['min'], term2_range['max'])
            if operation == '-' and b > a:
                a, b = b, a  # Ensure a >= b for subtraction
        elif operation == '×':
            a = random.randint(term1_range['min'], term1_range['max'])
            b = random.randint(term2_range['min'], term2_range['max'])
        else:  # division
            b = random.randint(term2_range['min'], term2_range['max'])
            a = b * random.randint(term1_range['min'], term1_range['max'])
        
        self.question = f"{a} {operation} {b}"
        if operation == '×':
            self.answer = a * b
        elif operation == '÷':
            self.answer = a / b
        else:
            self.answer = eval(f"{a} {'+' if operation == '+' else '-'} {b}")
        
        self.question_label.setText(self.question)
        self.answer_input.clear()
        self.answer_input.setFocus()
        self.current_operation = operation
        self.current_term1 = a
        self.current_term2 = b

    def check_answer(self):
        user_answer = self.answer_input.text()
        try:
            correct = abs(float(user_answer) - self.answer) < 1e-6
            if correct:
                self.score += 1
            self.questions_asked += 1
            self.score_label.setText(f'Score: {self.score}')
            
            # Add result to data manager
            self.data_manager.add_result(self.current_operation, self.current_term1, self.current_term2, correct)
            
            self.new_question()
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number.")

    def update_timer(self): 
        self.time_left -= 1
        self.time_label.setText(f'Time: {self.time_left}')
        if self.time_left <= 0:
            self.timer.stop()
            self.end_game()

    def end_game(self):
        self.data_manager.save_results()
        self.data_manager.create_heatmap()
        statistics = self.data_manager.get_statistics()
        self.results_window = ResultsWindow(self.score, self.questions_asked, self.start_time, statistics)
        self.results_window.show()
        self.close()