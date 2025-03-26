import joblib
import numpy as np
from tensorflow.keras.models import load_model

SAVE_DIR = "./models/"

def load_models():
    model = load_model('./models/ann_species_model.h5')
    scaler = joblib.load('./models/scaler.pkl')
    le = joblib.load('./models/label_encoder.pkl')

    return model, scaler, le

def start_predict(data):
    model,scaler,le = load_models()
    new_data_scaled = scaler.transform(data)
    predictions = model.predict(new_data_scaled)
    predicted_class = np.argmax(predictions, axis=1)
    predicted_species = le.inverse_transform(predicted_class)
    return_data = {
        "class" : predicted_species[0]
    }
    return return_data