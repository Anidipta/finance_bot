
import firebase_admin
from firebase_admin import credentials, firestore
from langchain.schema import Document
from datetime import datetime
import requests
import hashlib
import os

cred = credentials.Certificate("/content/gdg-25-firebase-adminsdk-fbsvc-1d7d00c3ee.json")  

if not firebase_admin._apps: 
    firebase_admin.initialize_app(cred)

GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID")
GA4_API_SECRET = os.getenv("GA4_API_SECRET")

db = firestore.client()
CHAT_COLLECTION = "user_chats"

def store_chat(user_id, email, message):
    """Store chat in Firestore and send event to Google Analytics."""
    chat_data = {
        "user_id": user_id,
        "email": email,
        "message": message,
        "timestamp": datetime.utcnow()
    }
    doc_ref = db.collection(CHAT_COLLECTION).add(chat_data)
    print("Chat message stored successfully!")

    GA4_ENDPOINT = f"https://www.google-analytics.com/mp/collect?measurement_id={GA4_MEASUREMENT_ID}&api_secret={GA4_API_SECRET}"

    event_data = {
        "client_id": user_id,
        "events": [{
            "name": "chat_message",
            "params": {
                "email_hash": hashlib.sha256(email.encode()).hexdigest(),
                "message": message,  
                "timestamp": chat_data["timestamp"].isoformat(),
                "debug_mode": 1
            }
        }]
    }
    
    response = requests.post(GA4_ENDPOINT, json=event_data)
    print("GA4 Event Sent:", response.status_code)
    print("Response Headers:", response.headers)

    import json
    print("Sent Data:", json.dumps(event_data, indent=4))

    return Document(page_content=message, metadata={"user_id": user_id, "email": email, "timestamp": chat_data["timestamp"]})

