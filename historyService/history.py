import uuid
from flask import jsonify, g
from firebase_admin import firestore

def create_history_entry(db, user_id, created_at, image_url, prediction):
    # Generate a unique history ID
    history_id = str(uuid.uuid4())

    # Create history data
    history_data = {
        "history_id": history_id,
        "userId": user_id,
        "createdAt": created_at,
        "image_url": image_url,
        "prediction": prediction
    }

    # Add document to Firestore
    db.collection('histories').document(history_id).set(history_data)

# Get all histories from a certain user
def get_histories():
    user_id = g.user_id
    db = firestore.client()
    histories = db.collection('histories').where('userId', '==', user_id).get()
    histories_data = [doc.to_dict() for doc in histories]
    
    if not histories_data:
        return jsonify({"message": "No histories found"}), 200
    
    return jsonify({"histories": histories_data}), 200

# Get history by history_id
def get_history_by_id(history_id):
    user_id = g.user_id
    db = firestore.client()
    history = db.collection('histories').document(history_id).get()
    if history.exists and history.to_dict()['userId'] == user_id:
        return jsonify({"history": history.to_dict()}), 200
    else:
        return jsonify({"error": "History not found or unauthorized access"}), 404

# Delete a history by the history_id
def delete_history_by_id(history_id):
    user_id = g.user_id
    db = firestore.client()
    history_ref = db.collection('histories').document(history_id)
    history = history_ref.get()
    if history.exists and history.to_dict()['userId'] == user_id:
        history_ref.delete()
        return jsonify({"message": "History deleted successfully"}), 200
    else:
        return jsonify({"error": "History not found or unauthorized access"}), 404

# Delete the all histories of the logged in user
def delete_all_histories():
    user_id = g.user_id
    db = firestore.client()
    histories = db.collection('histories').where('userId', '==', user_id).get()
    
    if not histories:
        return jsonify({"message": "No histories found to delete"}), 200

    for history in histories:
        history.reference.delete()
    
    return jsonify({"message": "All histories deleted successfully"}), 200

