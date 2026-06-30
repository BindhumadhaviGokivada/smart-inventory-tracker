import os
import pickle

import matplotlib

matplotlib.use("agg")  # Force non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.neural_network import MLPRegressor

from paths import DATA_PATH, MODEL_PATH, PLOT_DIR


def load_and_preprocess_data():
    """Load CSV and build raw quantity series (same units as /predict API inputs)."""
    try:
        data_path = DATA_PATH
        if not os.path.exists(data_path):
            raise FileNotFoundError(f"Data file not found at {data_path}")

        df = pd.read_csv(data_path)
        print(f"Loaded data with columns: {list(df.columns)}")

        if "quantity_stock" not in df.columns:
            raise ValueError("Required column 'quantity_stock' not found in data")

        df = df.sort_values("product_id")

        # Raw stock levels — matches quantity1/2/3 passed to model.predict() in app.py
        data = df["quantity_stock"].values.reshape(-1, 1).astype(np.float64)

        print(f"Preprocessed data shape: {data.shape}")
        return data, df
    except Exception as e:
        print(f"Error loading and preprocessing data: {str(e)}")
        return None, None


def create_sequences(data, time_steps=3):
    """Sliding-window features and targets."""
    try:
        X, y = [], []
        for i in range(len(data) - time_steps):
            X.append(data[i : (i + time_steps), 0])
            y.append(data[i + time_steps, 0])
        return np.array(X), np.array(y)
    except Exception as e:
        print(f"Error creating sequences: {str(e)}")
        return None, None


def build_sklearn_model(n_samples: int):
    """MLP for normal datasets; Ridge when too few samples for a neural net."""
    try:
        if n_samples < 4:
            return Ridge(alpha=1.0, random_state=42)
        return MLPRegressor(
            hidden_layer_sizes=(32, 16),
            max_iter=500,
            random_state=42,
            early_stopping=False,
            solver="lbfgs",
        )
    except Exception as e:
        print(f"Error building sklearn model: {str(e)}")
        return None


def train_model(model, X_train, y_train):
    """Fit sklearn regressor."""
    try:
        model.fit(X_train, y_train)
        return model
    except Exception as e:
        print(f"Error training model: {str(e)}")
        return None


def evaluate_model(model, X_train, y_train, X_test, y_test):
    """Metrics in raw quantity units."""
    try:
        train_predict = model.predict(X_train)
        train_predict = np.asarray(train_predict).reshape(-1, 1)
        y_train_2d = np.asarray(y_train).reshape(-1, 1)

        train_rmse = np.sqrt(mean_squared_error(y_train_2d, train_predict))
        train_mae = mean_absolute_error(y_train_2d, train_predict)
        print(f"Training RMSE: {train_rmse:.2f}")
        print(f"Training MAE: {train_mae:.2f}")

        if len(X_test) > 0 and len(y_test) > 0:
            test_predict = model.predict(X_test)
            test_predict = np.asarray(test_predict).reshape(-1, 1)
            y_test_2d = np.asarray(y_test).reshape(-1, 1)

            test_rmse = np.sqrt(mean_squared_error(y_test_2d, test_predict))
            test_mae = mean_absolute_error(y_test_2d, test_predict)
            print(f"Test RMSE: {test_rmse:.2f}")
            print(f"Test MAE: {test_mae:.2f}")
        else:
            test_predict = None
            y_test_2d = None

        return train_predict, test_predict, y_train_2d, y_test_2d
    except Exception as e:
        print(f"Error evaluating model: {str(e)}")
        return None, None, None, None


def save_model(model, scaler, filepath=None):
    """Save the trained model; scaler kept for pickle compatibility (may be None)."""
    if filepath is None:
        filepath = MODEL_PATH
    try:
        model_data = {"model": model, "scaler": scaler}
        with open(filepath, "wb") as f:
            pickle.dump(model_data, f)
        print(f"Model saved successfully to {filepath}")
        return True
    except Exception as e:
        print(f"Error saving model: {str(e)}")
        return False


def create_visualization(df, train_predict, test_predict, y_train_inv, y_test_inv):
    """Create and save visualization plots."""
    try:
        plt.figure(figsize=(12, 6))

        train_size = len(np.ravel(train_predict))
        plt.plot(
            range(train_size),
            np.ravel(y_train_inv),
            label="Actual (Train)",
            color="blue",
            marker="o",
        )
        plt.plot(
            range(train_size),
            np.ravel(train_predict),
            label="Predicted (Train)",
            color="red",
            marker="s",
        )

        if test_predict is not None and y_test_inv is not None:
            test_size = len(np.ravel(test_predict))
            plt.plot(
                range(train_size, train_size + test_size),
                np.ravel(y_test_inv),
                label="Actual (Test)",
                color="green",
                marker="o",
            )
            plt.plot(
                range(train_size, train_size + test_size),
                np.ravel(test_predict),
                label="Predicted (Test)",
                color="orange",
                marker="s",
            )

        plt.title("Stock level model: actual vs predicted", fontsize=16, fontweight="bold")
        plt.xlabel("Product Index", fontsize=12)
        plt.ylabel("Stock Quantity", fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)

        plot_path = os.path.join(PLOT_DIR, "sales_prediction_plot.png")
        plt.savefig(plot_path, dpi=300, bbox_inches="tight", facecolor="white")
        plt.close()

        print(f"Visualization saved to {plot_path}")
        return True
    except Exception as e:
        print(f"Error creating visualization: {str(e)}")
        return False


def main():
    """Train sklearn regressor on raw sequence features (TensorFlow-free for Vercel)."""
    try:
        print("Starting model training process...")

        print("Loading and preprocessing data...")
        data, df = load_and_preprocess_data()
        if data is None:
            print("Failed to load and preprocess data")
            return False

        if len(data) < 5:
            print(f"Not enough data for training. Need at least 5 samples, got {len(data)}")
            return False

        print("Creating sequences for sklearn regressor...")
        time_steps = min(3, len(data) - 1)
        X, y = create_sequences(data, time_steps)
        if X is None or len(X) == 0:
            print("Failed to create sequences or no sequences generated")
            return False

        if len(X) < 3:
            print(f"Not enough sequences for training. Need at least 3, got {len(X)}")
            return False

        train_size = max(1, int(len(X) * 0.8))
        X_train, X_test = X[:train_size], X[train_size:]
        y_train, y_test = y[:train_size], y[train_size:]

        print(f"Training set size: {len(X_train)}")
        print(f"Test set size: {len(X_test)}")

        print("Building sklearn model...")
        model = build_sklearn_model(len(X_train))
        if model is None:
            print("Failed to build model")
            return False

        print("Training model...")
        model = train_model(model, X_train, y_train)
        if model is None:
            print("Failed to train model")
            return False

        if len(X_test) > 0:
            print("Evaluating model...")
            train_predict, test_predict, y_train_inv, y_test_inv = evaluate_model(
                model, X_train, y_train, X_test, y_test
            )
            if train_predict is None:
                print("Failed to evaluate model")
                return False
        else:
            print("Making predictions on training data...")
            train_predict = model.predict(X_train)
            train_predict = np.asarray(train_predict).reshape(-1, 1)
            y_train_inv = np.asarray(y_train).reshape(-1, 1)
            test_predict = None
            y_test_inv = None

        print("Saving model...")
        if not save_model(model, None):
            print("Failed to save model")
            return False

        if len(X_train) > 2:
            print("Creating visualization...")
            create_visualization(df, train_predict, test_predict, y_train_inv, y_test_inv)

        print("Model training completed successfully!")
        return True

    except Exception as e:
        print(f"Error in main function: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("Model training process completed successfully!")
    else:
        print("Model training process failed!")
