import firebase_admin
from firebase_admin import credentials, auth, firestore

cred = credentials.Certificate("flask-1b27b-firebase-adminsdk-hqp4j-e6ebfc3716.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
