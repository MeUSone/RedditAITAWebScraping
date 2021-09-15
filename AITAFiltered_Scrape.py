import praw
import pandas as pd
from bs4 import BeautifulSoup
import pprint


reddit = praw.Reddit(
    client_id="BBADp-gSLgP2aeQyVh-Q9A",
    client_secret="WfdBLPPxj1rrlK6vmQTJKzGGO_cYtg",
    user_agent="my user agent",
    username="llama0627",
    password="Aa87287230",
)
# submission = reddit.submission(url="https://www.reddit.com/r/AmItheAsshole/comments/owe92v/aita_for_not_wanting_to_buy_kids_food_at_a/")
# print(submission.author)
# submission2 = reddit.submission(url="https://www.reddit.com/r/AmItheAsshole/comments/pob59q/aita_for_letting_my_wife_ground_my_daughter_my/")
# print(submission2.author)
subreddit = reddit.subreddit("AITAFiltered")
AITAFiltered = []
for submission in subreddit.hot(limit=1000):

# Get rid of the rule post
    if submission.stickied:
        continue
    print(submission.url)
    print(vars(submission))

#Get rid of the deleted posts
    if submission.crosspost_parent_list[0]['selftext'] == '[deleted]':
        continue

#Get rid of the posts posted twice
    if len(submission.comments)<1:
        continue
    cleanText = BeautifulSoup(submission.comments[0].body_html,"lxml").text

#Get rid of the posts that do not have a judgement form
    if("The final verdict" not in cleanText):
        continue

#Get the judgement from from HTML to string fromat and get the label
    cleanText = cleanText.replace("\n"," ").split("  ")
    print(cleanText)
    del cleanText[2]
    AITAFiltered.append({"Original_Post":submission.url,"JudgementForm":cleanText,"FinalResult":cleanText[0].split(":")[1]})
print(AITAFiltered)
dfAITAFiltered = pd.DataFrame(AITAFiltered)
dfAITAFiltered.to_csv('Posts.csv')