import os
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = os.getenv('BUCKET_NAME')

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
    suffix = 1
    base_name, extension = os.path.splitext(filename)
    while True:
        unique_filename = f"{folder_path}{base_name}_{suffix}{extension}"
        if not bucket.blob(unique_filename).exists():
            break
        suffix += 1
    
    # Create a blob object
    blob = bucket.blob(unique_filename)
    
    # Upload the image to GCS
    blob.upload_from_string(image_bytes, content_type='image/jpeg')
    
    # Make the blob publicly viewable
    blob.make_public()
    
    return blob.public_url
