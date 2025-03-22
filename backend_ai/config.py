import sys
import os

# Add the parent directory to sys.path to make absolute imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from firebase_admin import credentials, initialize_app
from google.cloud import firestore
from dotenv import load_dotenv
import os

load_dotenv()

cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS_PATH"))
firebase_app = initialize_app(cred)
db = firestore.Client()
