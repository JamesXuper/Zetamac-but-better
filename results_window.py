from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap

class ResultsWindow(QWidget):
    def __init__(self, score, total_questions, total_time, statistics):
        super().__init__()
        self.score = score
        self.total_questions = total_questions
        self.total_time = total_time
        self.statistics = statistics
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game Results')
        self.setGeometry(300, 300, 800, 600)
        
        layout = QVBoxLayout()
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        title_label = QLabel('Game Results', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        scroll_layout.addWidget(title_label)
        
        # Add game statistics
        self.add_statistic(scroll_layout, 'Score', f'{self.score}/{self.total_questions}')
        self.add_statistic(scroll_layout, 'Accuracy', f'{(self.score / self.total_questions) * 100:.2f}%' if self.total_questions > 0 else 'N/A')
        self.add_statistic(scroll_layout, 'Average Time per Question', f'{self.total_time / self.total_questions:.2f} seconds' if self.total_questions > 0 else 'N/A')
        
        # Add overall statistics
        self.add_statistic(scroll_layout, 'Total Questions (All Games)', self.statistics['Total Questions'])
        self.add_statistic(scroll_layout, 'Total Correct Answers (All Games)', self.statistics['Correct Answers'])
        self.add_statistic(scroll_layout, 'Overall Accuracy', self.statistics['Accuracy'])
        
        # Add performance by operation
        performance_label = QLabel('Performance by Operation:', self)
        performance_label.setFont(QFont('Arial', 18, QFont.Bold))
        scroll_layout.addWidget(performance_label)
        
        for operation, accuracy in self.statistics['Performance by Operation'].items():
            self.add_statistic(scroll_layout, f'{operation}', f'{accuracy:.2%}')
        
        # Add heatmap
        heatmap_label = QLabel('Performance Heatmap:', self)
        heatmap_label.setFont(QFont('Arial', 18, QFont.Bold))
        scroll_layout.addWidget(heatmap_label)
        
        heatmap = QLabel(self)
        pixmap = QPixmap('performance_heatmap.png')
        heatmap.setPixmap(pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        scroll_layout.addWidget(heatmap)
        
        self.play_again_button = QPushButton('Play Again', self)
        self.play_again_button.setFont(QFont('Arial', 18))
        self.play_again_button.clicked.connect(self.play_again)
        scroll_layout.addWidget(self.play_again_button)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        self.setLayout(layout)

    def add_statistic(self, layout, label, value):
        stat_label = QLabel(f'{label}: {value}', self)
        stat_label.setFont(QFont('Arial', 16))
        layout.addWidget(stat_label)

    def play_again(self):
        from menu_window import MenuWindow
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()