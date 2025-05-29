from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import joblib
import os
import time
import pandas as pd

class SnakeMLModel:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self.is_trained = False
        self.metrics_history = {
            'accuracy': [],
            'train_size': [],
            'timestamp': [],
            'cross_val_scores': []
        }

    def train(self, X, y):
        if len(X) == 0 or len(y) == 0:
            print("Warning: Empty training data!")
            return False

        print(f"Training with {len(X)} samples...")

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Evaluate on test set
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        # Perform cross-validation
        cv_scores = cross_val_score(self.model, X, y, cv=5)

        # Store metrics
        self.metrics_history['accuracy'].append(accuracy)
        self.metrics_history['train_size'].append(len(X))
        self.metrics_history['timestamp'].append(time.time())
        self.metrics_history['cross_val_scores'].append(cv_scores.mean())

        # Print evaluation results
        print(f"\nTraining Results:")
        print(f"Training samples: {len(X_train)}")
        print(f"Test samples: {len(X_test)}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Cross-validation score (mean): {cv_scores.mean():.4f}")
        print(f"Cross-validation scores: {cv_scores}")

        # Detailed classification report
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))

        # Confusion matrix
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

        # Print feature importance if available
        if hasattr(self.model, 'feature_importances_'):
            print("\nFeature Importances:")
            for i, importance in enumerate(self.model.feature_importances_):
                print(f"Feature {i}: {importance:.4f}")

        return True

    def predict(self, X):
        if not self.is_trained:
            raise Exception("Model is not trained yet.")
        return self.model.predict(X)

    def save(self, path):
        """Save model and training metrics to organized folders"""
        # Create base directories if they don't exist
        os.makedirs(os.path.dirname(path), exist_ok=True)

        # Get base filename without extension and without path
        base_filename = os.path.basename(os.path.splitext(path)[0])
        training_dir = os.path.join(os.path.dirname(os.path.dirname(path)), "training")

        # Create training directories if needed
        models_dir = os.path.join(training_dir, "models")
        metrics_dir = os.path.join(training_dir, "metrics")
        plots_dir = os.path.join(training_dir, "plots")

        for directory in [models_dir, metrics_dir, plots_dir]:
            os.makedirs(directory, exist_ok=True)

        # Save model file to models directory
        model_path = os.path.join(models_dir, f"{base_filename}.joblib")
        joblib.dump(self.model, model_path)

        # If original path is not in models dir, also save there for compatibility
        if not path.startswith(models_dir):
            joblib.dump(self.model, path)

        # Save metrics to metrics directory
        metrics_path = os.path.join(metrics_dir, f"{base_filename}_metrics.csv")
        pd.DataFrame(self.metrics_history).to_csv(metrics_path, index=False)

        # Generate and save learning curve to plots directory
        plot_path = os.path.join(plots_dir, f"{base_filename}_learning_curve.png")
        self.plot_learning_curve(plot_path)

        print(f"Model saved to {model_path}")
        print(f"Metrics history saved to {metrics_path}")
        print(f"Learning curve saved to {plot_path}")

    def load(self, path):
        """Load model and look for associated metrics"""
        # Try to load from the exact path first
        if os.path.exists(path):
            self.model = joblib.load(path)
            self.is_trained = True

            # Get base filename
            base_filename = os.path.basename(os.path.splitext(path)[0])
            training_dir = os.path.join(os.path.dirname(os.path.dirname(path)), "training")

            # Try to load metrics from organized location
            metrics_path = os.path.join(training_dir, "metrics", f"{base_filename}_metrics.csv")

            # If not found, check original location
            if not os.path.exists(metrics_path):
                metrics_path = os.path.splitext(path)[0] + "_metrics.csv"

            if os.path.exists(metrics_path):
                try:
                    df = pd.read_csv(metrics_path)
                    self.metrics_history = df.to_dict(orient='list')
                    print(f"Loaded metrics history from {metrics_path}")
                except Exception as e:
                    print(f"Could not load metrics history: {e}")
            else:
                print(f"No metrics history found for {base_filename}")
        else:
            raise FileNotFoundError(f"Model file not found at {path}")

    def plot_learning_curve(self, save_path=None):
        """Plot the learning curve to visualize how model improves over time"""
        if not self.metrics_history['accuracy']:
            print("No training history available to plot learning curve")
            return

        plt.figure(figsize=(12, 6))

        # Plot 1: Accuracy over training iterations
        plt.subplot(1, 2, 1)
        plt.plot(range(len(self.metrics_history['accuracy'])), self.metrics_history['accuracy'], marker='o')
        plt.title('Model Accuracy over Training Sessions')
        plt.xlabel('Training Session')
        plt.ylabel('Accuracy')
        plt.grid(True)

        # Plot 2: Accuracy vs Dataset Size
        plt.subplot(1, 2, 2)
        plt.plot(self.metrics_history['train_size'], self.metrics_history['accuracy'], marker='o')
        plt.title('Accuracy vs Dataset Size')
        plt.xlabel('Training Dataset Size')
        plt.ylabel('Accuracy')
        plt.grid(True)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            print(f"Learning curve saved to {save_path}")
        else:
            plt.show()
