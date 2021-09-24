import praw
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

submission = reddit.submission(url="https://www.reddit.com/r/AmItheAsshole/comments/prgv6a/aita_for_calling_my_boyfriend_a_bum_in_front_of/")

submission.comments.replace_more(limit=None)
comment_queue = submission.comments[:]
while comment_queue:
    comment = comment_queue.pop(0)
    if comment.author == "Judgement_Bot_AITA":
        continue
    print(comment.body)
    comment_queue.extend(comment.replies)
