import firebase_admin
from bs4 import BeautifulSoup
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os
import json
import praw


def initialize_firebase():
    creds = credentials.Certificate(json.loads(os.environ.get("firebase_auth")))
    firebase_admin.initialize_app(creds, {
        'databaseURL': 'https://social-acceptance-fc45b-default-rtdb.firebaseio.com/'
    })


def reddit_auth():
    reddit_instance = praw.Reddit(
        client_id=os.environ.get("client_id"),
        client_secret=os.environ.get("client_secret"),
        user_agent="my user agent",
        username=os.environ.get("username"),
        password=os.environ.get("password")
    )
    return reddit_instance


def scrape_data(reddit):
    global data
    data = {}

    subreddit = reddit.subreddit("AITAFiltered")

    counter = 1
    for submission in subreddit.hot(limit=2):

        # Get rid of the rule post
        if submission.stickied:
            continue

        # Get rid of the deleted posts
        if submission.crosspost_parent_list[0]['selftext'] == '[deleted]':
            continue

        # Get rid of the posts posted twice
        if len(submission.comments) < 1:
            continue
        clean_text = BeautifulSoup(submission.comments[0].body_html, "lxml").text

        # Get rid of the posts that do not have a judgement form
        if "The final verdict" not in clean_text:
            continue

        # Get the judgement from from HTML to string fromat and get the label
        clean_text = clean_text.replace("\n", " ").split("  ")

        del clean_text[2]

        data[counter] = {}

        data[counter]["post_id"] = submission.id
        data[counter]["title"] = submission.title
        data[counter]["date"] = submission.created_utc
        data[counter]["url"] = submission.url
        data[counter]["flair"] = submission.link_flair_text

        counter += 1


if __name__ == '__main__':
    load_dotenv()
    initialize_firebase()
    reddit = reddit_auth()
    scrape_data(reddit)


# {INT_ID: {"post_id": INT, "title": STRING, "date": STRING, "url": STRING,
# "flair": STRING, scoresFromAITAFiltered: {"YTA": INT, "NTA": INT, "ESH": INT, "NAH": INT, "INFO": INT},
# scoresCustom: {"YTA": INT, "NTA": INT, "ESH": INT, "NAH": INT, "INFO": INT}
# comments: []}}