import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os
import json
import praw

reddit = None


def initialize_firebase():
    creds = credentials.Certificate(json.loads(os.environ.get("firebase_auth")))
    firebase_admin.initialize_app(creds, {
        'databaseURL': 'https://social-acceptance-fc45b-default-rtdb.firebaseio.com/'
    })


def reddit_auth():
    global reddit
    reddit = praw.Reddit(
        client_id=os.environ.get("client_id"),
        client_secret=os.environ.get("client_secret"),
        user_agent="my user agent",
        username=os.environ.get("username"),
        password=os.environ.get("password")
    )


def scrape_data():
    print(reddit)


if __name__ == '__main__':
    load_dotenv()
    initialize_firebase()
    reddit_auth()
    scrape_data()

