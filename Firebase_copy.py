import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv, find_dotenv
import os
import json
import praw
import datetime
from bs4 import BeautifulSoup

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

def cleanForm(cleanText):
    JudgementForm = {}
    JudgementForm[cleanText[2].split(" ")[0]] = float(cleanText[2].split(" ")[1].strip('%'))/100
    for a in range(len(cleanText)-4):
        JudgementForm[cleanText[a+3].split(" ")[1]] = float(cleanText[a+3].split(" ")[2].strip('%'))/100
    return JudgementForm

def scrape_data():
    ref = db.reference('/')
    subreddit = reddit.subreddit("AITAFiltered")
    AITAFiltered = []
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
        cleanText = BeautifulSoup(submission.comments[0].body_html, "lxml").text

        # Get rid of the posts that do not have a judgement form
        if "The final verdict" not in cleanText:
            continue

        # Get the judgement from from HTML to string fromat and get the label
        cleanText = cleanText.replace("\n", " ").split("  ")
        del cleanText[2]
        cleanForm(cleanText)

        submissionOriginal = reddit.submission(url='https://www.reddit.com'+submission.url)

        total_votes = 0
        judgement = {"NTA": 0, "YTA": 0, "NAH": 0, "INFO": 0, "ESH": 0}
        for top_level_comment in submissionOriginal.comments:
            if hasattr(top_level_comment, "body") == False:
                continue
            if "NTA" in top_level_comment.body:
                if top_level_comment.ups > 0:
                    total_votes += top_level_comment.ups
                    judgement["NTA"] += top_level_comment.ups
            elif "YTA" in top_level_comment.body:
                if top_level_comment.ups > 0:
                    total_votes += top_level_comment.ups
                    judgement["YTA"] += top_level_comment.ups
            elif "NAH" in top_level_comment.body:
                if top_level_comment.ups > 0:
                    total_votes += top_level_comment.ups
                    judgement["NAH"] += top_level_comment.ups
            elif "INFO" in top_level_comment.body:
                if top_level_comment.ups > 0:
                    total_votes += top_level_comment.ups
                    judgement["INFO"] += top_level_comment.ups
            elif "ESH" in top_level_comment.body:
                if top_level_comment.ups > 0:
                    total_votes += top_level_comment.ups
                    judgement["ESH"] += top_level_comment.ups
        custom_score = {"NTA": round(judgement["NTA"] / total_votes,2), "YTA": round(judgement["YTA"] / total_votes,2),
                        "NAH": round(judgement["NAH"] / total_votes,2), "INFO": round(judgement["INFO"] / total_votes,2),
                        "ESH": round(judgement["ESH"] / total_votes,2)}

        JudgementForm = cleanForm(cleanText)

        date = '{0.month}/{0.day}/{0.year}'.format(datetime.datetime.utcfromtimestamp(submission.created_utc))

        ref.push({"INT_ID": {"post_id": submissionOriginal.author.name, "title": submission.title, "date": date, "url": 'https://www.reddit.com'+submission.url,"story":submissionOriginal.selftext,
"flair": cleanText[0].split(":")[1], "scoresFromAITAFiltered": JudgementForm,"scoresCustom": custom_score,"comments": []}})



if __name__ == '__main__':
    load_dotenv("/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/ATT23877.env")
    initialize_firebase()
    reddit_auth()
    scrape_data()

