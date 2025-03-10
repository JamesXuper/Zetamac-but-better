# menu_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QHBoxLayout, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIntValidator
from game_window import GameWindow

class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.default_ranges = {
            '+': {'term1': {'min': 1, 'max': 100}, 'term2': {'min': 1, 'max': 100}},
            '-': {'term1': {'min': 1, 'max': 100}, 'term2': {'min': 1, 'max': 100}},
            '×': {'term1': {'min': 1, 'max': 100}, 'term2': {'min': 1, 'max': 12}},
            '÷': {'term1': {'min': 1, 'max': 100}, 'term2': {'min': 1, 'max': 12}}
        }
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Arithmetic Game - Menu')
        self.setGeometry(300, 300, 600, 500)
        
        layout = QVBoxLayout()
        
        title_label = QLabel('Arithmetic Game', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        layout.addWidget(title_label)

        self.time_input = QLineEdit(self)
        self.time_input.setValidator(QIntValidator(1, 3600))
        self.time_input.setText('120')
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel('Time (seconds):'))
        time_layout.addWidget(self.time_input)
        layout.addLayout(time_layout)

        range_layout = QGridLayout()
        self.range_inputs = {}
        operations = ['+', '-', '×', '÷']
        for i, op in enumerate(operations):
            range_layout.addWidget(QLabel(f'{op}:'), i, 0)
            
            term1_layout = QHBoxLayout()
            term1_min = QLineEdit(self)
            term1_max = QLineEdit(self)
            term1_min.setValidator(QIntValidator())
            term1_max.setValidator(QIntValidator())
            term1_min.setText(str(self.default_ranges[op]['term1']['min']))
            term1_max.setText(str(self.default_ranges[op]['term1']['max']))
            term1_layout.addWidget(QLabel('Term 1:'))
            term1_layout.addWidget(term1_min)
            term1_layout.addWidget(QLabel('to'))
            term1_layout.addWidget(term1_max)
            range_layout.addLayout(term1_layout, i, 1)
            
            term2_layout = QHBoxLayout()
            term2_min = QLineEdit(self)
            term2_max = QLineEdit(self)
            term2_min.setValidator(QIntValidator())
            term2_max.setValidator(QIntValidator())
            term2_min.setText(str(self.default_ranges[op]['term2']['min']))
            term2_max.setText(str(self.default_ranges[op]['term2']['max']))
            term2_layout.addWidget(QLabel('Term 2:'))
            term2_layout.addWidget(term2_min)
            term2_layout.addWidget(QLabel('to'))
            term2_layout.addWidget(term2_max)
            range_layout.addLayout(term2_layout, i, 2)
            
            self.range_inputs[op] = {
                'term1': (term1_min, term1_max),
                'term2': (term2_min, term2_max)
            }
        
        layout.addLayout(range_layout)

        start_button = QPushButton('Start Game', self)
        start_button.clicked.connect(self.start_game)
        layout.addWidget(start_button)

        self.setLayout(layout)

    def start_game(self):
        try:
            time = int(self.time_input.text())
            if time <= 0:
                raise ValueError("Time must be a positive integer")

            ranges = {}
            for op, terms in self.range_inputs.items():
                ranges[op] = {}
                for term, (min_input, max_input) in terms.items():
                    min_val = int(min_input.text())
                    max_val = int(max_input.text())
                    if min_val >= max_val:
                        raise ValueError(f"Invalid range for {op} {term}")
                    ranges[op][term] = {'min': min_val, 'max': max_val}

            self.game_window = GameWindow(time, ranges)
            self.game_window.show()
            self.close()

        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))