import praw
import pprint
import datetime
#Initialize
reddit = praw.Reddit(
    client_id="BBADp-gSLgP2aeQyVh-Q9A",
    client_secret="WfdBLPPxj1rrlK6vmQTJKzGGO_cYtg",
    user_agent="my user agent",
    username="llama0627",
    password="Aa87287230",
)

subreddit = reddit.subreddit("AmItheAsshole")
#Create a dataframe
document = {'title':[],'story':[],'comment':[],'JudgeForm':[],'UpvoteNumberForToppestNTA':[],'UpvoteNumberForToppestESH':[],'UpvoteNumberForToppestYTA':[],'UpvoteNumberForToppestINFO':[],
           'PostDate':[],'PosterUserName':[],'result':[],'URL':[]}
#Scrape posts
for submission in subreddit.hot(limit=10):
    document["title"].append(submission.title)
    document["URL"].append(submission.url)
    document["PosterUserName"].append(submission.author)
    document["PostDate"].append(datetime.datetime.utcfromtimestamp(submission.created_utc))
    document["PosterUserName"].append(submission.selftext)
    commentsAll=[]
    for top_level_comment in submission.comments:
        commentInformation = {'commentor':[],'body':[],'score(upvotes)':[],'Judgement':[]}
        if(hasattr(top_level_comment,'author')==False):
            break
        commentInformation['commentor'].append(top_level_comment.author)
        commentInformation['body'].append(top_level_comment.body)
        commentInformation['score(upvotes)'].append(top_level_comment.score)
        if("NTA" in top_level_comment.body):
            commentInformation['Judgement'].append("NTA")
        elif("YTA" in top_level_comment.body):
            commentInformation['Judgement'].append("YTA")
        elif("NAH" in top_level_comment.body):
            commentInformation['Judgement'].append("NAH")
        elif("INFO" in top_level_comment.body):
            commentInformation['Judgement'].append("INFO")
        elif("ESH" in top_level_comment.body):
            commentInformation['Judgement'].append("ESH")
        else:
            commentInformation['Judgement'].append("N/A")
        commentsAll.append(commentInformation)
    document["comment"].append(commentsAll)

#Show one sample comment(the first one is the rules post so showed the second)
print("sample comment")
print(document["comment"][1][1])

#Show one sample post
print("sample post")
print(document["comment"][1])
submission = reddit.submission(url="https://www.reddit.com/r/AmItheAsshole/comments/pfaofg/aita_for_denying_girlfriends_friend28m_to_live/")

#Variables in Comment (we can select more varibles to scrape)
pprint.pprint(vars(submission.comments[0]))

#Variables in Post (we can select more varibles to scrape)
pprint.pprint(vars(submission))

