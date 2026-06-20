import joblib

MODEL_PATH = "exponentialsmoothing.pkl"

def load_model():
    model = joblib.load(MODEL_PATH)
    return model
