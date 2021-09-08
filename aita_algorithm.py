import praw

reddit = praw.Reddit(
    client_id="BBADp-gSLgP2aeQyVh-Q9A",
    client_secret="WfdBLPPxj1rrlK6vmQTJKzGGO_cYtg",
    user_agent="my user agent",
    username="llama0627",
    password="Aa87287230",
)

submission = reddit.submission(url="https://www.reddit.com/r/AmItheAsshole/comments/pjjt55/aita_for_reporting_a_theft_of_less_than_2/")

total_votes = 0
judgement = {"NTA": 0, "YTA": 0, "NAH": 0, "INFO": 0, "ESH": 0}

print(submission.comments.list())
print(reddit.comment(id="hbxc2on").body)
print(reddit.comment(id="hbxc2on").score)
print((reddit.comment(id="hbxc2on")).ups)
print((reddit.comment(id="hbxc2on")).downs)

# for top_level_comment in submission.comments:
#     if "NTA" in top_level_comment.body:
#         total_votes += top_level_comment.ups
#         judgement["NTA"] += top_level_comment.ups
#     elif "YTA" in top_level_comment.body:
#         total_votes += top_level_comment.ups
#         judgement["YTA"] += top_level_comment.ups
#     elif "NAH" in top_level_comment.body:
#         total_votes += top_level_comment.ups
#         judgement["NAH"] += top_level_comment.ups
#     elif "INFO" in top_level_comment.body:
#         total_votes += top_level_comment.ups
#         judgement["INFO"] += top_level_comment.ups
#     elif "ESH" in top_level_comment.body:
#         total_votes += top_level_comment.ups
#         judgement["ESH"] += top_level_comment.ups
#
# print(judgement["YTA"]/total_votes)
#
