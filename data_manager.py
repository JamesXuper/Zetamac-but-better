import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os
import numpy as np

class DataManager:
    def __init__(self):
        self.file_path = 'arithmetic_game_results.xlsx'
        self.df = self.load_or_create_dataframe()

    def load_or_create_dataframe(self):
        if os.path.exists(self.file_path):
            return pd.read_excel(self.file_path)
        else:
            return pd.DataFrame(columns=['Timestamp', 'Operation', 'Term1', 'Term2', 'Correct'])

    def add_result(self, operation, term1, term2, correct):
        new_row = {
            'Timestamp': datetime.now(),
            'Operation': operation,
            'Term1': int(term1),  # Ensure numeric
            'Term2': int(term2),  # Ensure numeric
            'Correct': int(correct)  # Convert bool to int
        }
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)

    def save_results(self):
        self.df.to_excel(self.file_path, index=False)

    def create_heatmap(self):
        if len(self.df) == 0:
            # If no data, create empty plot with message
            plt.figure(figsize=(10, 8))
            plt.text(0.5, 0.5, 'No data available yet', 
                    horizontalalignment='center',
                    verticalalignment='center')
            plt.savefig('performance_heatmap.png')
            plt.close()
            return

        operations = sorted(self.df['Operation'].unique())
        rows = (len(operations) + 1) // 2
        fig, axes = plt.subplots(rows, 2, figsize=(20, 10 * rows))
        fig.suptitle('Performance Heatmaps by Operation', fontsize=16)
        
        # Convert axes to 2D array if it's 1D
        if rows == 1:
            axes = axes.reshape(1, -1)

        for idx, operation in enumerate(operations):
            row = idx // 2
            col = idx % 2
            ax = axes[row, col]
            
            op_data = self.df[self.df['Operation'] == operation].copy()
            
            if len(op_data) > 0:
                # Create pivot table with numeric values
                pivot = pd.pivot_table(
                    op_data,
                    values='Correct',
                    index='Term1',
                    columns='Term2',
                    aggfunc='mean',
                    fill_value=np.nan
                )
                
                # Sort index and columns numerically
                pivot.index = pd.to_numeric(pivot.index)
                pivot.columns = pd.to_numeric(pivot.columns)
                pivot = pivot.sort_index()
                pivot = pivot.sort_index(axis=1)
                
                # Create heatmap
                sns.heatmap(
                    pivot,
                    ax=ax,
                    cmap='YlOrRd',
                    annot=True,
                    fmt='.2f',
                    cbar=True,
                    vmin=0,
                    vmax=1,
                    mask=pivot.isna()
                )
            else:
                ax.text(0.5, 0.5, f'No data for {operation}',
                       horizontalalignment='center',
                       verticalalignment='center',
                       transform=ax.transAxes)
            
            ax.set_title(f'Operation: {operation}')
            ax.set_xlabel('Term 2')
            ax.set_ylabel('Term 1')

        # Hide empty subplots if odd number of operations
        if len(operations) % 2 == 1:
            axes[rows-1, 1].set_visible(False)

        plt.tight_layout()
        plt.savefig('performance_heatmap.png', bbox_inches='tight', dpi=300)
        plt.close()

    def get_statistics(self):
        total_questions = len(self.df)
        if total_questions == 0:
            return {
                'Total Questions': 0,
                'Correct Answers': 0,
                'Accuracy': '0.00%',
                'Performance by Operation': {}
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
            'Performance by Operation': performance
        }