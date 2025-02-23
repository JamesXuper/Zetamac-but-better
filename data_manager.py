import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import numpy as np

class DataManager:
    def __init__(self):
        self.file_path = 'arithmetic_game_results.xlsx'
        self.current_sheet_name = self.generate_sheet_name()
        self.df = self.load_or_create_dataframe()
        self.last_question_time = datetime.now()

    def generate_sheet_name(self):
        # Generate a unique sheet name based on timestamp
        return f"Game_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    def load_or_create_dataframe(self):
        if os.path.exists(self.file_path):
            # File exists, but we'll create a new sheet
            return pd.DataFrame(columns=['Time_Taken_Seconds', 'Operation', 'Term1', 'Term2', 'Correct'])
        else:
            # Create new file and first sheet
            return pd.DataFrame(columns=['Time_Taken_Seconds', 'Operation', 'Term1', 'Term2', 'Correct'])

    def add_result(self, operation, term1, term2, correct):
        current_time = datetime.now()
        time_taken = (current_time - self.last_question_time).total_seconds()
        
        new_row = {
            'Time_Taken_Seconds': time_taken,
            'Operation': operation,
            'Term1': int(term1),
            'Term2': int(term2),
            'Correct': int(correct)
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        self.last_question_time = current_time

    def save_results(self):
        try:
            # Read existing Excel file if it exists
            if os.path.exists(self.file_path):
                with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a') as writer:
                    self.df.to_excel(writer, sheet_name=self.current_sheet_name, index=False)
            else:
                # Create new Excel file if it doesn't exist
                self.df.to_excel(self.file_path, sheet_name=self.current_sheet_name, index=False)
        except Exception as e:
            print(f"Error saving results: {e}")

    def get_all_game_statistics(self):
        """Get statistics for all games in the Excel file"""
        if not os.path.exists(self.file_path):
            return []

        all_stats = []
        excel_file = pd.ExcelFile(self.file_path)
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            if len(df) == 0:
                continue

            total_questions = len(df)
            correct_answers = df['Correct'].sum()
            accuracy = correct_answers / total_questions

            # Calculate performance by operation
            performance = {}
            for operation in df['Operation'].unique():
                op_data = df[df['Operation'] == operation]
                op_accuracy = op_data['Correct'].mean()
                performance[operation] = op_accuracy if not pd.isna(op_accuracy) else 0.0

            # Calculate average time per question
            avg_time = df['Time_Taken_Seconds'].mean()

            game_stats = {
                'Game Session': sheet_name,
                'Total Questions': total_questions,
                'Correct Answers': int(correct_answers),
                'Accuracy': f'{accuracy:.2%}',
                'Average Time per Question': f'{avg_time:.2f} seconds',
                'Performance by Operation': performance
            }
            all_stats.append(game_stats)

        return all_stats

    def get_statistics(self):
        """Get statistics for current game"""
        total_questions = len(self.df)
        if total_questions == 0:
            return {
                'Total Questions': 0,
                'Correct Answers': 0,
                'Accuracy': '0.00%',
                'Performance by Operation': {},
                'Game Session': self.current_sheet_name
            }

        correct_answers = self.df['Correct'].sum()
        accuracy = correct_answers / total_questions

        # Calculate performance by operation
        performance = {}
        for operation in self.df['Operation'].unique():
            op_data = self.df[self.df['Operation'] == operation]
            op_accuracy = op_data['Correct'].mean()
            performance[operation] = op_accuracy if not pd.isna(op_accuracy) else 0.0

        return {
            'Total Questions': total_questions,
            'Correct Answers': int(correct_answers),
            'Accuracy': f'{accuracy:.2%}',
            'Performance by Operation': performance,
            'Game Session': self.current_sheet_name
        }