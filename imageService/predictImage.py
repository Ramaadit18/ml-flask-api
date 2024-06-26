import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import os

# Define path
current_dir = os.path.dirname(os.path.abspath(__file__))
models_dir = os.path.join(current_dir, '..', 'models')
model_pest_path = os.path.join(models_dir, 'model_pest_detection.h5')
model_disease_path = os.path.join(models_dir, 'model_plant_disease.h5')

# Load the models
model_pest = tf.keras.models.load_model(model_pest_path)
model_disease = tf.keras.models.load_model(model_disease_path)

# Labels for the models
pest_labels = ["ants", "bees", "beetle", "caterpillar", "earthworms", "earwig", "grasshopper", "moth", "slug", "snail", "wasp", "weevil"]
disease_labels = [
    "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy", "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy", "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_", "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy", "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy", "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot", "Peach___healthy", "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy", "Potato___Early_blight",
    "Potato___Late_blight", "Potto___healthy", "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch", "Strawberry___healthy", "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
    "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot", "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy"
]

def preprocess_image(img):
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    return x

def predict_pest(img):
    x = preprocess_image(img)
    pred = model_pest.predict(x)
    max_prediction_score = np.max(pred)
    prediction_index = np.argmax(pred)
    result = "Unknown" if max_prediction_score < 0.87 else pest_labels[prediction_index]
    return result

def predict_disease(img):
    x = preprocess_image(img)
    pred = model_disease.predict(x)
    max_prediction_score = np.max(pred)
    prediction_index = np.argmax(pred)
    result = "Unknown" if max_prediction_score < 0.85 else disease_labels[prediction_index]
    return result
