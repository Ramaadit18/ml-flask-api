import os
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firestore():
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Path to the service account JSON file
    service_account_path = os.path.join(parent_dir, "service-account-firebase.json")

    # Initialize Firebase Admin SDK with service account credentials
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)
    return firestore.client()
