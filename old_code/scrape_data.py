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

    post_info = {counter: {"post_id": submission.id, "title": submission.title, "date": submission.created_utc,
                           "url": submission.url, "flair": submission.link_flair_text,
                           "scores_judgement_bot": {"YTA": 0, "NTA": 0, "ESH": 0, "NAH": 0, "INFO": 0},
                           "scores_custom": {"YTA": 0, "NTA": 0, "ESH": 0, "NAH": 0, "INFO": 0}, "comments": []}}

    clean_text = clean_text.replace("\n", " ").split("  ")
    del clean_text[2]
    clean_text = clean_text[2:-1]
    cleaned_text_list = []
    for b in range(0, len(clean_text)):
        cleaned_text_list.append(clean_text[b].strip()[:-1].split(" "))

    for i in cleaned_text_list:
        post_info[counter]["scores_judgement_bot"][i[0]] = int(i[1])


#
# # print(AITAFiltered)
# dfAITAFiltered = pd.DataFrame(AITAFiltered)
# dfAITAFiltered.to_csv('Posts_Raw.csv')
