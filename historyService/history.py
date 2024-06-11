from firebase_admin import firestore

def create_history_entry(db, user_id, created_at, image_url):
    # Create history data
    history_data = {
        "userId": user_id,
        "createdAt": created_at,
        "image_url": image_url
    }

    # Add document to Firestore
    db.collection('histories').add(history_data)
