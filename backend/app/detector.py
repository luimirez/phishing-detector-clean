import os
import pickle


#We have to create the path or route to the model as we are going to create it
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../ml/model.pkl')

model = None

#Loading  the model and create a vectorizer to the system and the pipeline model
def load_model():
    global model
    if model is None:
        try:
            with open(MODEL_PATH, 'rb') as f:
                model = pickle.load(f)
                print("✅ Model loaded successfully")
        except FileNotFoundError:
            print("❌ model.pkl not found at startup.")
            model = None
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            model = None

    return model