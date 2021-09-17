import praw
import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    user_agent="my user agent",
    username=os.environ.get("username"),
    password=os.environ.get("password")
)

subreddit = reddit.subreddit("AITAFiltered")
AITAFiltered = []
for submission in subreddit.hot(limit=1000):

    # Get rid of the rule post
    if submission.stickied:
        continue
    # print(submission.url)
    # print(vars(submission))

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
    # print(cleanText)
    del cleanText[2]
    AITAFiltered.append({"Original_Post": submission.url, "JudgementForm": cleanText,
                         "FinalResult": cleanText[0].split(":")[1]})

# print(AITAFiltered)
dfAITAFiltered = pd.DataFrame(AITAFiltered)
dfAITAFiltered.to_csv('Posts_Raw.csv')
