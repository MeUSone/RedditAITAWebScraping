import firebase_admin
from bs4 import BeautifulSoup
from firebase_admin import credentials, db
from dotenv import load_dotenv
import os
import json
import praw
import datetime
from psaw import PushshiftAPI

api = PushshiftAPI()


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
    subreddit = reddit.subreddit("AITAFiltered")
    counter = 1
    results = list(api.search_submissions(subreddit='AITAFiltered',limit=2))
    # for submission in subreddit.hot(limit=100000):

    for result in results:

        submission = reddit.submission(url=result.full_link)
        # Get rid of the rule post

        if submission.stickied:
            continue

        #Get rid of the deleted posts
        if submission.crosspost_parent_list[0]['selftext'] == '[deleted]':
            continue

        # Get rid of the posts posted twice
        if len(submission.comments) < 1:
            continue

        clean_text = BeautifulSoup(submission.comments[0].body_html, "lxml").text
        # Get rid of the posts that do not have a judgement form
        if "The final verdict" not in clean_text:
            continue

        post_info = {counter: {"post_id": submission.id, "title": submission.title, "date": '{0.month}/{0.day}/{0.year}'.format(datetime.datetime.utcfromtimestamp(submission.created_utc)),
                               "url": "https://www.reddit.com" + submission.url, "flair": submission.link_flair_text,
                               "body": "",
                               "scores_judgement_bot": {"YTA": 0, "NTA": 0, "ESH": 0, "NAH": 0, "INFO": 0},
                               "scores_custom": {}, "comments": []}}

        clean_text = clean_text.replace("\n", " ").split("  ")
        del clean_text[2]
        clean_text = clean_text[2:-1]
        cleaned_text_list = []
        for b in range(0, len(clean_text)):
            cleaned_text_list.append(clean_text[b].strip()[:-1].split(" "))

        for i in cleaned_text_list:
            post_info[counter]["scores_judgement_bot"][i[0]] = int(i[1])

        submission_aita = reddit.submission(url=post_info[counter]["url"])

        total_votes = 0
        judgement = {"NTA": 0, "YTA": 0, "NAH": 0, "INFO": 0, "ESH": 0}
        submission_aita.comments.replace_more(limit=None)
        comment_queue = submission_aita.comments[:]
        while comment_queue:
            comment = comment_queue.pop(0)
            if comment.author == "Judgement_Bot_AITA":
                continue
            if comment.author == None:
                continue
            post_info[counter]["comments"].append ({"comment_author": comment.author.name, "comment_body": comment.body,
                        "comment_ups": comment.ups})
            comment_queue.extend(comment.replies)

        for top_level_comment in submission_aita.comments:
            if not hasattr(top_level_comment, "body"):
                continue
            if top_level_comment.author == None:
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
        post_info[counter]["scores_custom"] = {"YTA": round((judgement["YTA"] / total_votes) * 100, 3),
                                               "NTA": round((judgement["NTA"] / total_votes) * 100, 3),
                                               "ESH": round((judgement["ESH"] / total_votes) * 100, 3),
                                               "NAH": round((judgement["NAH"] / total_votes) * 100, 3),
                                               "INFO": round((judgement["INFO"] / total_votes) * 100, 3)}

        post_info[counter]["body"] = submission_aita.selftext

        ref = db.reference()
        #ref.push(post_info)
        print(post_info)
        counter += 1


if __name__ == '__main__':
    load_dotenv("/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/ATT23877.env")
    initialize_firebase()
    reddit = reddit_auth()
    api = PushshiftAPI()
    scrape_data(reddit)

