import firebase_admin
from firebase_admin import credentials, firestore_async

# Initialize Firebase with your credentials (ensure you have 'firebase-adminsdk.json' in your project directory)
cred = credentials.Certificate('firebase-adminsdk.json')
firebase_admin.initialize_app(cred)

# Create a Firestore client instance
db = firestore_async.client()