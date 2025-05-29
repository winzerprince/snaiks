#!/usr/bin/env python3
# train_model.py - Script to train the snake ML model

import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from ml.agent import SnakeAgent
from settings import ML_DATA_LOG_PATH
import datetime
import shutil

def count_lines_in_file(file_path):
    """Count the number of non-empty lines in a file"""
    with open(file_path, 'r') as f:
        return sum(1 for line in f if line.strip())

def main():
    print("\n===== Snake ML Model Training =====")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create training directory structure
    training_dir = os.path.join(os.path.dirname(__file__), "training")
    models_dir = os.path.join(training_dir, "models")
    metrics_dir = os.path.join(training_dir, "metrics")
    plots_dir = os.path.join(training_dir, "plots")

    for directory in [models_dir, metrics_dir, plots_dir]:
        os.makedirs(directory, exist_ok=True)

    # Create an agent
    agent = SnakeAgent()

    # Check if the log file exists
    if not os.path.exists(ML_DATA_LOG_PATH):
        print(f"Error: Training data file not found at {ML_DATA_LOG_PATH}")
        print("Run the game first to generate training data!")
        return

    # Get file size and data statistics
    file_size = os.path.getsize(ML_DATA_LOG_PATH) / (1024 * 1024)  # Size in MB
    num_samples = count_lines_in_file(ML_DATA_LOG_PATH)
    print(f"Found training data file: {ML_DATA_LOG_PATH}")
    print(f"File size: {file_size:.2f} MB")
    print(f"Number of training samples: {num_samples}")

    # If the file is very small, warn the user
    if num_samples < 100:
        print("\nWARNING: Very few training samples available.")
        print("Consider playing the game more to generate additional data.")
        if input("Continue with training anyway? (y/n): ").lower() != 'y':
            return

    # Check for existing model to see learning progress
    model_path = "trained_snake_model.joblib"
    models_model_path = os.path.join(models_dir, "trained_snake_model.joblib")

    # First check if model exists in new organized location
    if os.path.exists(models_model_path):
        print(f"\nFound existing model at {models_model_path}")
        try:
            agent.model.load(models_model_path)
            if agent.model.metrics_history['accuracy']:
                print("\nPrevious training metrics:")
                print(f"Last accuracy: {agent.model.metrics_history['accuracy'][-1]:.4f}")
                print(f"Dataset size: {agent.model.metrics_history['train_size'][-1]}")
        except Exception as e:
            print(f"Error loading existing model: {e}")
            print("Will train a new model instead")
    # If not found in organized location, check old location
    elif os.path.exists(model_path):
        print(f"\nFound existing model at {model_path}")
        try:
            agent.model.load(model_path)
            if agent.model.metrics_history['accuracy']:
                print("\nPrevious training metrics:")
                print(f"Last accuracy: {agent.model.metrics_history['accuracy'][-1]:.4f}")
                print(f"Dataset size: {agent.model.metrics_history['train_size'][-1]}")
        except Exception as e:
            print(f"Error loading existing model: {e}")
            print("Will train a new model instead")

    # Train the model
    print("\nTraining model from log data...")
    try:
        success = agent.train_from_log(ML_DATA_LOG_PATH)
        if success:
            print("Training completed successfully!")

            # Save the trained model with timestamp to the organized folder structure
            timestamped_model_name = f"trained_snake_model_{timestamp}"
            model_path = os.path.join(models_dir, f"{timestamped_model_name}.joblib")
            agent.save_model(model_path)

            # Also save to standard name for the game to use (both in root and models dir)
            standard_model_path = os.path.join(models_dir, "trained_snake_model.joblib")
            agent.save_model(standard_model_path)

            # Copy the standard model to root directory for backwards compatibility
            root_model_path = "trained_snake_model.joblib"
            shutil.copy2(os.path.join(models_dir, "trained_snake_model.joblib"), root_model_path)
            print(f"Default model also saved to {root_model_path} for backwards compatibility")

            # Show training directory structure
            print(f"\nTraining data is now organized in the training/ directory:")
            print(f"  - Models saved in: {models_dir}")
            print(f"  - Metrics saved in: {metrics_dir}")
            print(f"  - Learning curves saved in: {plots_dir}")

            # Show learning progress
            print("\nTo see if the model is learning, check:")
            print(f"1. The accuracy values in the training output above")
            print(f"2. The learning curve plots in {plots_dir}")
            print("3. Run the game and observe if AI snakes perform better")

            print("\nSigns the model is learning well:")
            print("- Increasing accuracy over time")
            print("- Consistent cross-validation scores")
            print("- Feature importances that make logical sense")
            print("- AI snakes in the game exhibiting more intelligent behavior")

            print("\nIf accuracy is low or not improving:")
            print("- Generate more training data by playing the game longer")
            print("- Try adjusting the model parameters or using a different algorithm")
            print("- Check the quality of the training data")
        else:
            print("Training was not successful. Check the logs for details.")
    except Exception as e:
        print(f"Error during training: {e}")

if __name__ == "__main__":
    main()
