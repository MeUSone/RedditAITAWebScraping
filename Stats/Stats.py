import numpy as np
import json
import re
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict

def statsAITA(filename):
    f = open(filename,"r")
    data = f.read()
    content_list = data.splitlines()
    document = []
    for content in content_list:
        document.append(json.loads(content))

    tokenizer = RegexpTokenizer(r'\w+')

    commentSum = 0
    commentSet = []

    upvotesAll = 0
    upvotesAllSet = []
    upvotesAvaPerComment = 0
    upvotesAvaPerCommentSet = []
    commentLengthSet = []

    lengthPerStory = 0
    lengthPerStorySet = []
    lengthPerStoryChar = 0
    lengthPerStoryCharSet = []

    flairAll = defaultdict(int)

    userAll = 0

    poster = set()
    for a in range(0,len(document)):
        upvotes = 0

        commentSum+=len(document[a][str(a+1)]["comments"])
        commentSet.append(len(document[a][str(a+1)]["comments"]))

        lengthPerStory+=len(document[a][str(a+1)]['body'].split())
        lengthPerStorySet.append(len(document[a][str(a+1)]['body'].split()))
        lengthPerStoryChar+=len(document[a][str(a+1)]['body'])
        lengthPerStoryCharSet.append(len(document[a][str(a+1)]['body']))

        user = set()

        flairAll[document[a][str(a+1)]["flair"]] = flairAll[document[a][str(a+1)]["flair"]]+1

        poster.add(document[a][str(a+1)]['post_id'])
        for comment in document[a][str(a+1)]["comments"]:
            upvotes+=comment["comment_ups"]
            user.add(comment['comment_author'])
            commentbody = tokenizer.tokenize(comment['comment_body'])
            commentLengthSet.append(len(commentbody))

        userAll+=len(user)

        upvotesAvaPerComment +=upvotes/len(document[a][str(a+1)]["comments"])
        upvotesAvaPerCommentSet.append(upvotes/len(document[a][str(a+1)]["comments"]))
        upvotesAll+=upvotes
        upvotesAllSet.append(upvotes)

    commentAverage = commentSum/len(document)
    upvotesAvaPerComment = upvotesAvaPerComment/len(document)
    upvotesAverage = upvotesAll/len(document)
    lengthPerStory = lengthPerStory/len(document)
    lengthPerStoryChar = lengthPerStoryChar/len(document)
    userAvarage = userAll/len(document)


    print('For posts in ',filename,' The stats is below: total posts collected: ',len(document),', average comments per post: ',commentAverage,
          ', average upvotes per post: ',upvotesAverage,', average upvotes per comment: ',upvotesAvaPerComment,
          ', average length per story: ',lengthPerStory,', average characters per story: ',lengthPerStoryChar,
          ', average unique user comment per story: ',userAvarage,', unique story poster: ',len(poster))
    print(flairAll)
    plt.hist(upvotesAllSet,bins=20,range=(0,10000))
    plt.title('Upvotes per post')
    plt.show()

    plt.hist(upvotesAvaPerCommentSet,bins=20)
    plt.title('Upvotes per comment')
    plt.show()

    plt.hist(lengthPerStorySet,bins=20)
    plt.title('length per story')
    plt.show()

    plt.hist(lengthPerStoryCharSet,bins=20)
    plt.title('Character length per story')
    plt.show()

    plt.hist(commentLengthSet,bins=20,range=(0,1000))
    plt.title("Comment length")
    plt.show()

    with open(filename+".json", "w") as outfile:
        json.dump(document, outfile)


def statsAITAWithDate(filename):
    f = open(filename,"r")
    data = f.read()
    content_list = data.splitlines()
    document = []
    for content in content_list:
        document.append(json.loads(content))

    tokenizer = RegexpTokenizer(r'\w+')
    commentSet = []
    upvotesAllSet = []
    upvotesAvaPerCommentSet = []
    commentLengthSet = []
    lengthPerStorySet = []
    lengthPerStoryCharSet = []
    flairAll = defaultdict(int)

    commentSum = 0
    upvotesAll = 0
    upvotesAvaPerComment = 0
    lengthPerStory = 0
    lengthPerStoryChar = 0
    userAll = 0
    poster = set()
    commentTimeAve = timedelta(days=0)
    for a in range(0,len(document)):
        upvotes = 0
        commentTimeSum = timedelta(days=0)
        commentSum+=len(document[a][str(a+1)]["comments"])
        lengthPerStory+=len(document[a][str(a+1)]['body'].split())
        lengthPerStoryChar+=len(document[a][str(a+1)]['body'])
        user = set()
        poster.add(document[a][str(a+1)]['post_id'])
        for comment in document[a][str(a+1)]["comments"]:

            upvotes+=comment["comment_ups"]
            user.add(comment['comment_author'])
            commentTimeSum+= datetime.strptime(comment["comment_datetime_UTC"], '%Y-%m-%d %H:%M:%S')-\
                             datetime.strptime(document[a][str(a+1)]["UTC datetime"], '%Y-%m-%d %H:%M:%S')
            commentbody = tokenizer.tokenize(comment['comment_body'])
            commentLengthSet.append(len(commentbody))

        userAll+=len(user)
        upvotesAvaPerComment +=upvotes/len(document[a][str(a+1)]["comments"])
        upvotesAll+=upvotes
        commentTimeAve+=commentTimeSum/len(document[a][str(a+1)]["comments"])
        commentSet.append(len(document[a][str(a + 1)]["comments"]))
        lengthPerStorySet.append(len(document[a][str(a + 1)]['body'].split()))
        lengthPerStoryCharSet.append(len(document[a][str(a + 1)]['body']))
        flairAll[document[a][str(a + 1)]["flair"]] = flairAll[document[a][str(a + 1)]["flair"]] + 1
        upvotesAvaPerCommentSet.append(upvotes / len(document[a][str(a + 1)]["comments"]))
        upvotesAllSet.append(upvotes)


    commentAverage = commentSum/len(document)
    upvotesAvaPerComment = upvotesAvaPerComment/len(document)
    upvotesAverage = upvotesAll/len(document)
    lengthPerStory = lengthPerStory/len(document)
    lengthPerStoryChar = lengthPerStoryChar/len(document)
    userAvarage = userAll/len(document)
    commentTimeAve=commentTimeAve/len(document)
    print(flairAll)
    plt.hist(upvotesAllSet, bins=20, range=(0, 10000))
    plt.title('Upvotes per post')
    plt.show()

    plt.hist(upvotesAvaPerCommentSet, bins=20)
    plt.title('Upvotes per comment')
    plt.show()

    plt.hist(lengthPerStorySet, bins=20)
    plt.title('length per story')
    plt.show()

    plt.hist(lengthPerStoryCharSet, bins=20)
    plt.title('Character length per story')
    plt.show()

    plt.hist(commentLengthSet, bins=20, range=(0, 1000))
    plt.title("Comment length")
    plt.show()

    print('For posts in ',filename,' The stats is below: total posts collected: ',len(document),', average comments per post: ',commentAverage,
          ', average upvotes per post: ',upvotesAverage,', average upvotes per comment: ',upvotesAvaPerComment,
          ', average length per story: ',lengthPerStory,', average characters per story: ',lengthPerStoryChar,
          ', average unique user comment per story: ',userAvarage,', unique story poster: ',len(poster))
    print("average comment time: ",commentTimeAve)

    with open(filename+".json", "w") as outfile:
        json.dump(document, outfile)

def statsAITAFilter(filename):
    f = open(filename,"r")
    data = f.read()
    content_list = data.splitlines()
    document = []
    for content in content_list:
        document.append(json.loads(content))

    lengthPerStory = 0
    lengthPerStoryChar = 0
    lengthPerStorySet = []
    lengthPerStoryCharSet = []
    poster = set()
    flairAll = defaultdict(int)

    for a in range(0,len(document)):
        lengthPerStory+=len(document[a][str(a+1)]['body'].split())
        lengthPerStoryChar+=len(document[a][str(a+1)]['body'])
        poster.add(document[a][str(a+1)]['post_id'])
        lengthPerStorySet.append(len(document[a][str(a + 1)]['body'].split()))
        lengthPerStoryCharSet.append(len(document[a][str(a + 1)]['body']))
        flairAll[document[a][str(a + 1)]["flair"]] = flairAll[document[a][str(a + 1)]["flair"]] + 1

    lengthPerStory = lengthPerStory/len(document)
    lengthPerStoryChar = lengthPerStoryChar/len(document)



    print('For posts in ',filename,' The stats is below: total posts collected: ',len(document),
          ', average length per story: ',lengthPerStory,', average characters per story: ',lengthPerStoryChar,', unique story poster: ',len(poster))

    plt.hist(lengthPerStorySet, bins=20)
    plt.title('length per story')
    plt.show()

    plt.hist(lengthPerStoryCharSet, bins=20)
    plt.title('Character length per story')
    plt.show()

    with open(filename+".json", "w") as outfile:
        json.dump(document, outfile)

if __name__ == '__main__':
    #statsAITA('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_Sep20-Oct6.txt')
    # statsAITA('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_Sep1-Sep20.txt')
    # statsAITA('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_Oct6-After.txt')
    # statsAITAWithDate('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_May1-Jun1.txt')
    # statsAITAWithDate('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_Mar1-Apr1.txt')
    # statsAITA('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_Jun1-Jul1.txt')
    # statsAITA('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_Jul1-Aug1.txt')
    #statsAITAWithDate('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_Jan1-Feb1.txt')
    # #stats('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_Feb1-Mar1.txt')
    # statsAITA('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_Aug1-Sep1.txt')
    # statsAITA('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITA/AITA_Apr1-May1.txt')
    # print("Total posts: ",3641+4368+3983+4439+2375+4529+6203+5723+7053+3941)
    statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_Sep20-Oct6.txt')
    # statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_Sep1-Sep20.txt')
    # statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_Oct6-After.txt')
    # statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_May1-Jun1.txt')
    # statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_Mar1-Apr1.txt')
    # statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_Jun1-Jul1.txt')
    # statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_Jul1-Aug1.txt')
    # statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_Jan1-Feb1.txt')
    # statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_Feb1-Mar1.txt')
    # statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_Aug1-Sep1.txt')
    # statsAITAFilter('/Users/jiayifu/Desktop/NLP2021Fall/RedditAITAWebScraping/Stats/output/AITAFiltered/Filtered_Apr1-May1.txt')
    print("Total posts: ", 92+86+88+121+70+112+144+146+108+167+92)