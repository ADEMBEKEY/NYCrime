import joblib
import numpy as np
import os

MODEL_PATH = os.path.join("models", "lgbm.joblib")
try:
    model = joblib.load(MODEL_PATH)
    print(f"Model type: {type(model)}")
    if hasattr(model, 'predict_proba'):
        print("Model supports predict_proba")
    else:
        print("Model does NOT support predict_proba")
except Exception as e:
    print(f"Error: {e}")
