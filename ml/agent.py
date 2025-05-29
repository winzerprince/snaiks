# ml/agent.py: (Placeholder) RL Agent class that will wrap the NN model

import numpy as np
from .model import SnakeMLModel
import os

class SnakeAgent:
    def __init__(self, model_path=None):
        self.model = SnakeMLModel()
        if model_path and os.path.exists(model_path):
            self.model.load(model_path)

    def load_training_data(self, log_path):
        X, y = [], []
        line_count = 0
        valid_count = 0

        print("Loading training data...")
        with open(log_path, 'r') as f:
            for line in f:
                line_count += 1
                try:
                    parts = line.strip().split(',')
                    if len(parts) < 13:  # We expect at least 12 features + 1 label
                        continue

                    *features, label = parts
                    # Convert features to float, handling potential errors
                    feature_values = [float(x) for x in features]

                    # Skip rows with NaN or infinity values
                    if not all(np.isfinite(val) for val in feature_values):
                        continue

                    X.append(feature_values)
                    y.append(label)
                    valid_count += 1
                except Exception as e:
                    if line_count < 10:
                        print(f"Error parsing line: {e}")
                        print(f"Problematic line: {line[:100]}...")

        print(f"Processed {line_count} lines from log file")
        print(f"Found {valid_count} valid training samples")

        if valid_count == 0:
            print("No valid training data found! Check the format of your log file.")
            return np.array([]), np.array([])

        return np.array(X), np.array(y)

    def train_from_log(self, log_path):
        X, y = self.load_training_data(log_path)
        if len(X) == 0:
            return False

        # Print distribution of actions in training data
        unique_actions, action_counts = np.unique(y, return_counts=True)
        print("\nAction distribution in training data:")
        for action, count in zip(unique_actions, action_counts):
            print(f"  {action}: {count} samples ({count/len(y)*100:.1f}%)")

        # Train the model with the enhanced training method
        return self.model.train(X, y)

    def predict(self, features):
        X = np.array(features).reshape(1, -1)
        return self.model.predict(X)[0]

    def save_model(self, path):
        self.model.save(path)

    def evaluate_in_game_performance(self, game_stats):
        """
        Analyze game performance metrics to see if AI snakes are improving

        Parameters:
        - game_stats: dict with metrics like survival_time, food_eaten, etc.

        Returns:
        - Performance summary
        """
        return {
            'summary': "Performance metrics being collected...",
            'improving': True if game_stats.get('food_eaten', 0) > 5 else False
        }
