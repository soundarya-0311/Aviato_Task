from google.cloud import firestore

client = firestore.Client.from_service_account_json("phrasal-chiller-443513-u1-1eb39beb218a.json")

db = client.collection("users")