import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import numpy as np
from flask import Flask, request, jsonify, g
from PIL import Image
import io
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from google.cloud import storage
from datetime import datetime
from middleware.verifyToken import token_required
import requests
from dotenv import load_dotenv
from firebaseConfig.firebase import initialize_firestore
from historyService.history import create_history_entry

load_dotenv()

BUCKET_NAME = os.getenv('BUCKET_NAME')

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './service-account-pest-sentry.json'

app = Flask(__name__)

# Load the model
model = tf.keras.models.load_model('model_pest_detection.h5')
label = ["ants", "bees", "beetle", "caterpillar", "earthworms", "earwig", "grasshopper", "moth", "slug", "snail", "wasp", "weevil"]

# Initialize Firebase Admin SDK
db = initialize_firestore()

@app.route('/predict', methods=['POST'])
@token_required
def index():
    file = request.files['file']
    if file is None or file.filename == "":
        return jsonify({"error": "no file"})
    
    # Read the image bytes
    image_bytes = file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    
    # Get prediction
    pred_img = predict_label(img)

    # Access the user_id from Flask's g object
    user_id = g.user_id

    # Save the image to GCS and get the public URL
    image_url = save_image_to_gcs(image_bytes, file.filename, user_id)

    # Create history entry
    create_history_entry(db, user_id, datetime.utcnow().isoformat() + 'Z', image_url)
    
    return jsonify({"prediction": pred_img, "user_id": user_id, "image_url": image_url}), 200

def predict_label(img):
    # Preprocess the image
    img = img.resize((224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    
    # Make predictions
    pred = model.predict(x)
    result = label[np.argmax(pred)]
    return result

def save_image_to_gcs(image_bytes, filename, user_id):
    # Initialize a Cloud Storage client
    client = storage.Client()
    bucket = client.bucket(BUCKET_NAME)

    # Construct the folder path using the user's ID
    folder_path = f"{user_id}/"

    # Check if the folder exists, create it if it doesn't
    blob = bucket.blob(folder_path)
    if not blob.exists():
        blob.upload_from_string('')

    # Generate the unique filename prefix
    prefix = 1
    while True:
        unique_filename = f"{folder_path}{prefix}_{filename}"
        if not bucket.blob(unique_filename).exists():
            break
        prefix += 1
    
    # Create a blob object
    blob = bucket.blob(unique_filename)
    
    # Upload the image to GCS
    blob.upload_from_string(image_bytes, content_type='image/jpeg')
    
    # Make the blob publicly viewable
    blob.make_public()
    
    return blob.public_url

if __name__ == "__main__":
    app.run(debug=True)
