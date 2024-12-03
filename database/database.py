import os
from google.cloud import firestore

credential_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
client = firestore.Client.from_service_account_json(credential_path)

db = client.collection("users")