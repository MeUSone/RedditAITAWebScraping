import json
import os

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, db

load_dotenv()

creds = credentials.Certificate(json.loads(os.environ.get("firebase_auth")))
firebase_admin.initialize_app(creds, {
    'databaseURL': 'https://social-acceptance-fc45b-default-rtdb.firebaseio.com/'})

ref = db.reference().delete()
