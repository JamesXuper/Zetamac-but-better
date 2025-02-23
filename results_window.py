from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel, 
                           QScrollArea, QTableWidget, QTableWidgetItem, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QColor

class ResultsWindow(QWidget):
    def __init__(self, score, total_questions, total_time, statistics, question_history):
        super().__init__()
        self.score = score
        self.total_questions = total_questions
        self.total_time = total_time
        self.statistics = statistics
        self.question_history = question_history
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Game Results')
        self.setGeometry(300, 300, 1200, 800)
        
        layout = QVBoxLayout()
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Current Game Tab
        current_game_tab = QWidget()
        current_game_layout = QVBoxLayout()
        
        title_label = QLabel('Current Game Results', self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Bold))
        current_game_layout.addWidget(title_label)
        
        # Add game statistics
        self.add_statistic(current_game_layout, 'Game Session', self.statistics['Game Session'])
        self.add_statistic(current_game_layout, 'Score', f'{self.score}/{self.total_questions}')
        self.add_statistic(current_game_layout, 'Accuracy', 
                          f'{(self.score / self.total_questions) * 100:.2f}%' if self.total_questions > 0 else 'N/A')
        self.add_statistic(current_game_layout, 'Average Time per Question', 
                          f'{self.total_time / self.total_questions:.2f} seconds' if self.total_questions > 0 else 'N/A')
        
        # Add question history table
        history_label = QLabel('Question History:', self)
        history_label.setFont(QFont('Arial', 18, QFont.Bold))
        current_game_layout.addWidget(history_label)
        
        current_game_layout.addWidget(self.create_question_history_table())
        
        current_game_tab.setLayout(current_game_layout)
        
        # All Games History Tab
        all_games_tab = QWidget()
        all_games_layout = QVBoxLayout()
        
        all_games_title = QLabel('All Games History', self)
        all_games_title.setAlignment(Qt.AlignCenter)
        all_games_title.setFont(QFont('Arial', 24, QFont.Bold))
        all_games_layout.addWidget(all_games_title)
        
        # Add table with all games history
        all_games_layout.addWidget(self.create_all_games_table())
        
        all_games_tab.setLayout(all_games_layout)
        
        # Add tabs to tab widget
        tab_widget.addTab(current_game_tab, "Current Game")
        tab_widget.addTab(all_games_tab, "All Games History")
        
        layout.addWidget(tab_widget)
        
        # Play Again button
        self.play_again_button = QPushButton('Play Again', self)
        self.play_again_button.setFont(QFont('Arial', 18))
        self.play_again_button.clicked.connect(self.play_again)
        layout.addWidget(self.play_again_button)
        
        self.setLayout(layout)

    def create_question_history_table(self):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['Question', 'Your Answer', 'Correct Answer', 'Result'])
        table.setRowCount(len(self.question_history))
        table.setMinimumHeight(300)
        
        for i, record in enumerate(self.question_history):
            question_item = QTableWidgetItem(record['question'])
            user_answer_item = QTableWidgetItem(str(record['user_answer']))
            correct_answer_item = QTableWidgetItem(str(record['correct_answer']))
            result_item = QTableWidgetItem('Correct' if record['is_correct'] else 'Incorrect')
            
            if record['is_correct']:
                result_item.setBackground(QColor(144, 238, 144))  # Light green
            else:
                result_item.setBackground(QColor(255, 182, 193))  # Light red
            
            table.setItem(i, 0, question_item)
            table.setItem(i, 1, user_answer_item)
            table.setItem(i, 2, correct_answer_item)
            table.setItem(i, 3, result_item)
        
        table.resizeColumnsToContents()
        return table

    def create_all_games_table(self):
        from data_manager import DataManager
        all_stats = DataManager().get_all_game_statistics()
        
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            'Game Session', 
            'Total Questions', 
            'Correct Answers', 
            'Accuracy',
            'Avg Time/Question',
            'Performance by Operation'
        ])
        table.setRowCount(len(all_stats))
        
        for i, game in enumerate(all_stats):
            session_item = QTableWidgetItem(game['Game Session'])
            total_q_item = QTableWidgetItem(str(game['Total Questions']))
            correct_item = QTableWidgetItem(str(game['Correct Answers']))
            accuracy_item = QTableWidgetItem(game['Accuracy'])
            time_item = QTableWidgetItem(game['Average Time per Question'])
            
            # Format performance by operation as a string
            performance_str = ', '.join(
                [f"{op}: {acc:.2%}" for op, acc in game['Performance by Operation'].items()]
            )
            performance_item = QTableWidgetItem(performance_str)
            
            table.setItem(i, 0, session_item)
            table.setItem(i, 1, total_q_item)
            table.setItem(i, 2, correct_item)
            table.setItem(i, 3, accuracy_item)
            table.setItem(i, 4, time_item)
            table.setItem(i, 5, performance_item)
        
        table.resizeColumnsToContents()
        return table

    def add_statistic(self, layout, label, value):
        stat_label = QLabel(f'{label}: {value}', self)
        stat_label.setFont(QFont('Arial', 16))
        layout.addWidget(stat_label)

    def play_again(self):
        from menu_window import MenuWindow
        self.menu_window = MenuWindow()
        self.menu_window.show()
        self.close()