from google.cloud import firestore

client = firestore.Client()

db = client.collection("users")