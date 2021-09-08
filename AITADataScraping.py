import praw
import pprint
import datetime
import pandas as pd

reddit = praw.Reddit(
    client_id="BBADp-gSLgP2aeQyVh-Q9A",
    client_secret="WfdBLPPxj1rrlK6vmQTJKzGGO_cYtg",
    user_agent="my user agent",
    username="llama0627",
    password="Aa87287230",
)

subreddit = reddit.subreddit("AmItheAsshole")
#Create a dataframe
document= {'title':[],'story':[],'comment':[],'JudgeForm':[],'UpvoteNumberForToppestNTA':[],'UpvoteNumberForToppestESH':[],'UpvoteNumberForToppestYTA':[],'UpvoteNumberForToppestINFO':[],
           'PostDate':[],'PosterUserName':[],'result':[],'URL':[]}
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
        commentInformation['commentor']=top_level_comment.author
        commentInformation['body']=top_level_comment.body
        commentInformation['upvotes']=top_level_comment.ups
        if("NTA" in top_level_comment.body):
            commentInformation['Judgement']="NTA"
        elif("YTA" in top_level_comment.body):
            commentInformation['Judgement']="YTA"
        elif("NAH" in top_level_comment.body):
            commentInformation['Judgement']="NAH"
        elif("INFO" in top_level_comment.body):
            commentInformation['Judgement']="INFO"
        elif("ESH" in top_level_comment.body):
            commentInformation['Judgement']="ESH"
        else:
            commentInformation['Judgement']="N/A"
        commentsAll.append(commentInformation)
        commentsAlldf = pd.DataFrame(commentsAll)
    document["comment"].append(commentsAlldf)

#Show one sample comment(the first one is the rules post so showed the second)
print("sample comment")
print(document["comment"][1])

#Try one post from AITAFilted to see if we could repreduce the Judgement Form (No could not do it. Reason need to be investigated)
submission = reddit.submission(url="https://www.reddit.com/r/AmItheAsshole/comments/pjda60/aita_for_wanting_a_phone_jail_at_my_wedding/")

dt= {'title':[],'story':[],'comment':[],'JudgeForm':[],'UpvoteNumberForToppestNTA':[],'UpvoteNumberForToppestESH':[],'UpvoteNumberForToppestYTA':[],'UpvoteNumberForToppestINFO':[],
           'PostDate':[],'PosterUserName':[],'result':[],'URL':[]}
dt["title"].append(submission.title)
dt["URL"].append(submission.url)
dt["PosterUserName"].append(submission.author)
dt["PostDate"].append(datetime.datetime.utcfromtimestamp(submission.created_utc))
dt["PosterUserName"].append(submission.selftext)
commentsAll=[]
for top_level_comment in submission.comments:
    commentInformation = {'commentor':[],'body':[],'score(upvotes)':[],'Judgement':[]}
    if(hasattr(top_level_comment,'author')==False):
        break
    commentInformation['commentor']=top_level_comment.author
    commentInformation['body']=top_level_comment.body
    commentInformation['upvotes']=top_level_comment.ups
    if("NTA" in top_level_comment.body):
        commentInformation['Judgement']="NTA"
    elif("YTA" in top_level_comment.body):
        commentInformation['Judgement']="YTA"
    elif("NAH" in top_level_comment.body):
        commentInformation['Judgement']="NAH"
    elif("INFO" in top_level_comment.body):
        commentInformation['Judgement']="INFO"
    elif("ESH" in top_level_comment.body):
        commentInformation['Judgement']="ESH"
    else:
        commentInformation['Judgement']="N/A"
    commentsAll.append(commentInformation)
    commentsAlldf = pd.DataFrame(commentsAll)
dt["comment"].append(commentsAlldf)

#Try to get the algorithm for judgement form
df = pd.DataFrame(dt['comment'][0])
df.sort_values('upvotes',ascending = False).head(100)
df.groupby('Judgement')['upvotes'].nlargest().reset_index()
#371+1+9+11
#According to the judgement form the toppest comment is 371YTA and it is 54%, then the NTA(28%) should be 192 upvotes
#but I could not find one such comment even when I mutrually looking at the original post
