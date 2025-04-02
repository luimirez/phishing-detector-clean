import os
import pickle


#We have to create the path or route to the model as we are going to create it
MODEL_PATH = os.path.join(os.path.dirname(__file__), '../../ml/model.pkl')

#Loading  the model and create a vectorizer to the system and the pipeline model
try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
except Exception as e:
    print(f"Failed to load model: {e}")
    raise

def is_phishing(text: str) -> bool:
    try:
        
        prediction = model.predict([text])
        return bool(prediction[0]) # we are trying to convert numpy.bool into native bool
    except Exception as e:
        print(f"Prediction error: {e}")
        raise