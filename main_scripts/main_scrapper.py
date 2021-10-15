import operator

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
    limit = 2
    counter = 1
    reddit_data = {}
    results = list(api.search_submissions(subreddit='AITAFiltered', limit=limit))

    for result in results:

        submission = reddit.submission(url=result.full_link)
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

        original_url = "https://www.reddit.com" + submission.url

        original_submission = reddit.submission(url=original_url)

        post_info = {"post_id": submission.id, "title": submission.title,
                     "date": '{0.month}/{0.day}/{0.year}'.format(
                         datetime.datetime.utcfromtimestamp(submission.created_utc)),
                     "url": original_submission.url,
                     "flair": original_submission.link_flair_text.strip(), "body": "",
                     "scores_judgement_bot": {"YTA": 0, "NTA": 0, "ESH": 0, "NAH": 0, "INFO": 0},
                     "scores_custom": {}, "comments": []}

        clean_text = clean_text.replace("\n", " ").split("  ")
        del clean_text[2]
        clean_text = clean_text[2:-1]
        cleaned_text_list = []
        for b in range(0, len(clean_text)):
            cleaned_text_list.append(clean_text[b].strip()[:-1].split(" "))

        for i in cleaned_text_list:
            post_info["scores_judgement_bot"][i[0]] = int(i[1])

        submission_aita = reddit.submission(url=post_info["url"])

        submission_aita.comments.replace_more(limit=None)
        comment_queue = [[x, 'TOP-LEVEL COMMENT', 'TOP-LEVEL COMMENT'] for x in submission_aita.comments[:]]
        while comment_queue:
            comment = comment_queue.pop(0)
            if comment[0].author is None or comment[0].author == "Judgement_Bot_AITA":
                continue
            post_info["comments"].append({"comment_id": comment[0].id, "comment_author": comment[0].author.name,
                                          "comment_body": comment[0].body, "comment_ups": comment[0].ups,
                                          "parent_comment_id": comment[1],
                                          "parent_author": comment[2]})
            comment_queue.extend([[x, comment[0].id, comment[0].author.name] for x in comment[0].replies])

        judgement = {"NTA": 0, "YTA": 0, "NAH": 0, "INFO": 0, "ESH": 0}
        for top_level_comment in submission_aita.comments:
            if not hasattr(top_level_comment, "body") or top_level_comment.author is None:
                continue
            comment = top_level_comment.body.upper()
            if "NTA" in comment:
                if top_level_comment.ups > 0:
                    judgement["NTA"] = max(top_level_comment.ups, judgement["NTA"])
            elif "YTA" in comment:
                if top_level_comment.ups > 0:
                    judgement["YTA"] = max(top_level_comment.ups, judgement["YTA"])
            elif "NAH" in comment:
                if top_level_comment.ups > 0:
                    judgement["NAH"] = max(top_level_comment.ups, judgement["NAH"])
            elif "INFO" in comment:
                if top_level_comment.ups > 0:
                    judgement["INFO"] = max(top_level_comment.ups, judgement["INFO"])
            elif "ESH" in comment:
                if top_level_comment.ups > 0:
                    judgement["ESH"] = max(top_level_comment.ups, judgement["ESH"])
        total_votes = sum(judgement.values())
        post_info["scores_custom"] = {"NTA": round((judgement["NTA"] / total_votes) * 100),
                                      "YTA": round((judgement["YTA"] / total_votes) * 100),
                                      "NAH": round((judgement["NAH"] / total_votes) * 100),
                                      "INFO": round((judgement["INFO"] / total_votes) * 100),
                                      "ESH": round((judgement["ESH"] / total_votes) * 100)}

        post_info["body"] = submission_aita.selftext

        flair_map = {"Not the A-hole": "NTA", "Asshole": "YTA", "Not Enough Info": "INFO",
                                         "Everyone Sucks": "ESH", "No A-holes": "NAH"}
        converted_flair = flair_map[post_info["flair"]]
        customized_vote = max(post_info["scores_custom"], key=post_info["scores_custom"].get)
        judgement_form_vote = max(post_info["scores_judgement_bot"], key=post_info["scores_judgement_bot"].get)

        post_info["customized_algorithm/flair"] = converted_flair == customized_vote
        post_info["customized_algorithm/judgement_form"] = customized_vote == judgement_form_vote
        post_info["judgement_form/flair"] = judgement_form_vote == converted_flair

        reddit_data[counter] = post_info
        counter += 1

    print(reddit_data)


if __name__ == '__main__':
    load_dotenv()
    reddit = reddit_auth()
    api = PushshiftAPI()
    scrape_data(reddit)
