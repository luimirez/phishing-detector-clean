import os
import pickle

# Resolve the absolute path to model.pkl
MODEL_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../ml/model.pkl'))

model = None

def load_model():
    """Load and return the phishing detection model."""
    global model
    if model is None:
        try:
            print(f"📁 Loading model from: {MODEL_PATH}")
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
                print("Model loaded successfully.")
        except FileNotFoundError:
            print("model.pkl not found at startup.")
            model = None
        except Exception as e:
            print(f"Failed to load model: {e}")
            model = None

    return model

def is_phishing(text: str) -> bool:
    """Check if the given text is phishing using the model."""
    clf = load_model()
    if clf is None:
        raise RuntimeError("Model not loaded.")
    prediction = clf.predict([text])[0]
    return bool(prediction)
