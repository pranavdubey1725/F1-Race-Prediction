import joblib
import os
import numpy as np
from typing import Optional

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")

_model_cache = {}


def load_model(model_name: str = "f1_model"):
    """Load a .pkl or .joblib model from the models/ directory. Cached after first load."""
    if model_name in _model_cache:
        return _model_cache[model_name]

    for ext in [".joblib", ".pkl"]:
        path = os.path.join(MODEL_DIR, f"{model_name}{ext}")
        if os.path.exists(path):
            model = joblib.load(path)
            _model_cache[model_name] = model
            print(f"[ModelLoader] Loaded model from: {path}")
            return model

    print(f"[ModelLoader] No model file found for '{model_name}'. Using mock predictor.")
    return None


class MockPredictor:
    """
    Fallback mock predictor for when no trained model is found.
    Simulates realistic predictions based on input features.
    """

    def predict(self, X: np.ndarray) -> np.ndarray:
        np.random.seed(int(X[0][0]) if len(X) > 0 else 42)
        positions = np.clip(
            np.round(np.random.normal(loc=10, scale=5, size=len(X))).astype(int),
            1, 20
        )
        return positions

    def predict_proba(self, X: np.ndarray) -> Optional[np.ndarray]:
        return None


def get_predictor(model_name: str = "f1_model"):
    model = load_model(model_name)
    if model is None:
        return MockPredictor()
    return model