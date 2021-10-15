import pandas as pd
import praw, os
import numpy as np
from dotenv import load_dotenv

load_dotenv()

df = pd.read_csv("old_code/Post_Cleaned.csv")

reddit = praw.Reddit(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    user_agent="my user agent",
    username=os.environ.get("username"),
    password=os.environ.get("password")
)

data_reddit = [[]]*len(df.index)

for reddit_url in range(0,len(df)):
    print(reddit_url)
    submission = reddit.submission(url=df["Post_url"][reddit_url])

    total_votes = 0
    judgement = {"NTA": 0, "YTA": 0, "NAH": 0, "INFO": 0, "ESH": 0}

    for top_level_comment in submission.comments:
        if hasattr(top_level_comment,"body")==False:
            continue
        comment = top_level_comment.body.upper()[0:30]
        if "NTA" in comment:
            if top_level_comment.ups > 0:
                judgement["NTA"] = max(top_level_comment.ups,judgement["NTA"])
        elif "YTA" in comment:
            if top_level_comment.ups > 0:
                judgement["YTA"] = max(top_level_comment.ups,judgement["YTA"])
        elif "NAH" in comment:
            if top_level_comment.ups > 0:
                judgement["NAH"] = max(top_level_comment.ups,judgement["NAH"])
        elif "INFO" in comment:
            if top_level_comment.ups > 0:
                judgement["INFO"] = max(top_level_comment.ups,judgement["INFO"])
        elif "ESH" in comment:
            if top_level_comment.ups > 0:
                judgement["ESH"] = max(top_level_comment.ups,judgement["ESH"])

    total_votes = sum(judgement.values())
    custom_score = {"NTA": judgement["NTA"]/total_votes, "YTA": judgement["YTA"]/total_votes,
                    "NAH": judgement["NAH"]/total_votes, "INFO": judgement["INFO"]/total_votes,
                    "ESH": judgement["ESH"]/total_votes}
    data = list(custom_score.items())

    data = sorted(data, key=lambda x: x[1],reverse=True)

    data_reddit[reddit_url] = data

df["Custom Score"] = data_reddit
df.drop('Unnamed: 0', axis=1, inplace=True)
abbreviation_form={" Not the A-hole":"NTA"," Asshole":"YTA"," Not Enough Info":"INFO"," Everyone Sucks":"ESH"," No A-holes":"NAH"," No A-holes here":"NAH"}
temp = []
for a in range(len(df)):
    temp.append(df["Custom Score"][a][0][0] == abbreviation_form.get(df["FinalResult"][a]))
df["Same Label"] = temp
df.to_csv("old_code/post_new.csv")

