import pandas as pd
import praw
import numpy as np

df = pd.read_csv("Post_Cleaned.csv")

reddit = praw.Reddit(
    client_id="BBADp-gSLgP2aeQyVh-Q9A",
    client_secret="WfdBLPPxj1rrlK6vmQTJKzGGO_cYtg",
    user_agent="my user agent",
    username="llama0627",
    password="Aa87287230",
)

data_reddit = [[]]*len(df.index)

for reddit_url in range(0,2):
    submission = reddit.submission(url=df["Post_url"][reddit_url])

    total_votes = 0
    judgement = {"NTA": 0, "YTA": 0, "NAH": 0, "INFO": 0, "ESH": 0}

    for top_level_comment in submission.comments:
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

    custom_score = {"NTA": judgement["NTA"]/total_votes, "YTA": judgement["YTA"]/total_votes,
                    "NAH": judgement["NAH"]/total_votes, "INFO": judgement["INFO"]/total_votes,
                    "ESH": judgement["ESH"]/total_votes}
    data = list(custom_score.items())

    data_reddit[reddit_url] = data

df["Custom Score"] = data_reddit
df.drop('Unnamed: 0', axis=1, inplace=True)

print(df)

