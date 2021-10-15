import json
import os

import firebase_admin, praw
from dotenv import load_dotenv
from firebase_admin import credentials, db

load_dotenv()

# creds = credentials.Certificate(json.loads(os.environ.get("firebase_auth")))
# firebase_admin.initialize_app(creds, {
#     'databaseURL': 'https://social-acceptance-fc45b-default-rtdb.firebaseio.com/'})
#
# ref = db.reference().delete()

reddit = praw.Reddit(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    user_agent="my user agent",
    username=os.environ.get("username"),
    password=os.environ.get("password")
)

submission = reddit.submission(url="https://www.reddit.com/r/AmItheAsshole/comments/q5v9d5/aita_for_moving_out_midlease_without_telling_my/")

print("NTA" in "nta")