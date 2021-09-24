import praw
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup

load_dotenv()

reddit = praw.Reddit(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    user_agent="my user agent",
    username=os.environ.get("username"),
    password=os.environ.get("password")
)
submission = reddit.submission(
    url="https://www.reddit.com/r/AmItheAsshole/comments/ptm80l/aita_for_telling_my_coworker_that_its_not_my/")

total_votes = 0
judgement = {"NTA": 0, "YTA": 0, "NAH": 0, "INFO": 0, "ESH": 0}

for top_level_comment in submission.comments:
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

custom_score = {"YTA": judgement["YTA"] / total_votes,
                "NTA": judgement["NTA"] / total_votes,
                "ESH": judgement["ESH"] / total_votes,
                "NAH": judgement["NAH"] / total_votes,
                "INFO": judgement["INFO"] / total_votes}

print(custom_score)